import sys
import cv2
import os
import tempfile
import numpy as np

from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from ultralytics import YOLO
from moviepy.video.fx import all as vfx
from moviepy.editor import VideoFileClip, ImageClip, ColorClip, AudioFileClip, CompositeAudioClip, \
    concatenate_audioclips
from moviepy.video.compositing.concatenate import concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

console = Console()

nothing_or_something = 'nothing'
start = 0
end = 3.86666
exception1 = False
exception2 = False
read_screen_bool = True
model_path = ''
threshold = 0.5
amount_frames_to_skip = 2
detections = 0
detection_already_found = False
regular_editing = 0


def absolute_paths(specifiedpath):
    return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), specifiedpath)


def generate_text_image(text, font_size, font_color, vid_width, vid_height):
    image = Image.new("RGB", (vid_width, vid_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(font_size)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    text_position = ((vid_width - w) // 2, (vid_height - h) // 2)
    draw.text(text_position, text, font=font, fill=font_color)
    if not os.path.exists(absolute_paths("output_images")):
        os.makedirs(absolute_paths("output_images"))
    image.save(absolute_paths(f"output_images/{text}.png"))


# Function to create a black screen with text
def create_intro_text_clip(text, vid_width, vid_height):
    black_screen = ColorClip(size=(vid_width, vid_height), color=(0, 0, 0), duration=3)
    generate_text_image(text, 100, (255, 255, 255), vid_width, vid_height)
    text_clip = ImageClip(absolute_paths(f"output_images/{text}.png"), duration=3)
    intro_clip = CompositeVideoClip([black_screen, text_clip.set_duration(3)])
    intro_clip = intro_clip.fadeout(0.6)
    intro_clip = intro_clip.fadein(0.6)
    return intro_clip


def replace_non_white_with_black(image):
    # Define the white color range
    lower_bound = np.array([217, 217, 217])  # 240 remember
    upper_bound = np.array([255, 255, 255])

    # Create a mask where pixels are within the defined range
    mask = np.all((image >= lower_bound) & (image <= upper_bound), axis=-1)

    # Replace non-white pixels with black
    image[~mask] = [0, 0, 0]

    return image


def crop_the_frame(height, width, frame, regular_check):
    rl_width = 5
    if regular_check == 2:
        regular_check = 0
        rl_width = 3
    start_y = ((height // 2) + int((200 * height) / 1440)) * regular_check
    end_y = start_y + (height // 4) - (int((100 * height) / 1440)) * regular_check
    start_x = width // 3
    end_x = start_x + (width // rl_width)
    return frame[start_y:end_y, start_x:end_x]


def auto_game_montage(*args):
    global path_to_video, amount_frames_to_skip, detections, start, end, read_screen_bool, model_path, threshold, regular_editing
    music_volume = args[3] / 100
    if args[7] == '':  # args[7] is the intro text that the user typed from the GUI (or none)
        no_intro_text = True
    else:
        no_intro_text = False
        start = 3
        end = 6.86666
    if args[6] == 'no':
        turn_off_effects = True
    else:
        turn_off_effects = False
    detections = 0
    path_to_video = args[0]
    output_filename = os.path.splitext(os.path.basename(path_to_video))[0]
    if ';' in args[0]:
        video_file_paths = args[0].split(';')
        video_clips = [VideoFileClip(file_path) for file_path in video_file_paths]
        concatenated_clip = concatenate_videoclips(video_clips, method="compose")
        path_to_video = os.path.join(tempfile.gettempdir(), "tempVID_AJKLF176.mp4")
        print("Program: Combining your clips...")
        concatenated_clip.write_videofile(path_to_video, logger=None)  # TODO: user should be able to adjust this 1
        print("Program: Done combining clips.")
        for clip in video_clips:
            clip.close()
    if not os.path.isabs(args[2]):
        if args[2] == 'none':
            music_choice = absolute_paths('editing_sfx/none.mp3')
        else:
            music_choice = absolute_paths('default_audio/' + args[2])
    else:
        music_choice = args[2]

    cap = cv2.VideoCapture(path_to_video)  # TODO: user should be able to adjust this 1

    # Get the video frame width, height, and frames per second (fps), make sure it's the right resolution
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    valid_heights = [480, 720, 1080, 1440, 2160]
    valid_widths = [640, 1280, 1920, 2560, 3840]
    if frame_height not in valid_heights or frame_width not in valid_widths:
        print(f"Your video resolution is {frame_width}x{frame_height}, it needs to be one of these resolutions: "
              f"640x480, 1280x720, 1920x1080, 2560x1440, 3840x2160")
        return

    cap.set(cv2.CAP_PROP_POS_MSEC, 3100)  # start at 3 seconds due to hardcoded edits
    ret, frame = cap.read()
    track_frames = []
    clips_list = []
    audio_clips_list = []
    which_game = args[4]
    read_screen_bool = False
    amount_frames_to_skip = args[5]

    if which_game == "CSGO":
        model_path = absolute_paths(r"YOLOmodels/csgo.pt")
    elif which_game == "Valorant":
        model_path = absolute_paths(r"YOLOmodels/valorant.pt")
    elif which_game == "Overwatch":
        threshold = 0.45
        model_path = absolute_paths(r"YOLOmodels/overwatch.pt")
    elif which_game == "Minecraft (PVP server)":
        model_path = absolute_paths(r"YOLOmodels/minecraft.pt")
    else:
        amount_frames_to_skip = int((fps * 25) / 60)
        threshold = 0.6
        regular_editing = 0
        if which_game == "Fortnite":
            threshold = 0.2
            regular_editing = 1
        if which_game == "MW 2019" or which_game == "PUBG PC":
            threshold = 0.7
        if which_game == "Rocket League":
            threshold = 0.46
            regular_editing = 2
        read_screen_bool = True
    model = YOLO(model_path)
    original_clip = VideoFileClip(path_to_video)  # TODO: user should be able to adjust this 1
    audio_clip = AudioFileClip(music_choice)  # TODO: user should be able to adjust this 1
    print(
        "------------------------------------------------------------------------------------------------------------")
    console.print(
        "             THIS QUOTE COMES FROM JESUS, READ IT WHILE YOU WAIT FOR THE PROGRAM TO FINISH                    ",
        style="bold red")
    print("------------------------------------------------------------------------------------------------------------"
          "\nDo not let your hearts be troubled. You believe in God; believe also in me. "
          "\nMy Father’s house has many rooms; if that were not so, would I have told you that "
          "\nI am going there to prepare a place for you? And if I go and prepare a place for "
          "\nyou, I will come back and take you to be with me that you also may be where I am. "
          "\nYou know the way to the place where I am going."
          "\nThomas said to him, Lord, we don’t know where you are going, so how can we know the way?"
          "\nJesus answered, I am the way and the truth and the life. No one comes to the Father except through me. "
          "\nIf you really know me, you will know my Father as well. From now on, you do know him and have seen him."
          "\nPhilip said, Lord, show us the Father and that will be enough for us."
          "\nJesus answered: Don’t you know me, Philip, even after I have been among you such a long time? "
          "\nAnyone who has seen me has seen the Father. How can you say, ‘Show us the Father’? "
          "\nDon’t you believe that I am in the Father, and that the Father is in me? The words "
          "\nI say to you I do not speak on my own authority. Rather, it is the Father, living in me, "
          "\nwho is doing his work. Believe me when I say that I am in the Father and the Father is in me; "
          "\nor at least believe on the evidence of the works themselves. Very truly I tell you, "
          "\nwhoever believes in me will do the works I have been doing, and they will do even greater things than these, "
          "\nbecause I am going to the Father. And I will do whatever you ask in my name, "
          "\nso that the Father may be glorified in the Son. You may ask me for anything in my name, and I will do it."
          "\n                                                  - John 14:1-14"
          "\n-------------------------------------------------------------------------------------------------------------")

    while ret:  # iterating through the video frames and skipping 1 every iteration
        current_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
        sys.stdout.flush()
        sys.stdout.write(
            f'\rModel: I\'m watching {str(current_timestamp / 60000)[:6]} minute(s) in your video | Detections: {detections}  ')
        global nothing_or_something, exception1, exception2
        exception1 = False
        exception2 = False
        nothing_or_something = 'nothing'

        def read_screen():
            # Finding the directory for the proper resolution of the template image (480,720,1080,etc folders)
            templates = []
            specified_res_dir = absolute_paths(rf"template_matching_resolutions/{str(frame_height)}p")
            for filename in os.listdir(specified_res_dir):
                if which_game.replace(" ", "") in filename:
                    templates.append(cv2.imread(specified_res_dir + rf"/{filename}", cv2.IMREAD_COLOR))
            global detection_already_found
            for template in templates:
                if detection_already_found:
                    detection_already_found = False
                    break
                # Perform template matching
                if regular_editing == 0 or regular_editing == 2:
                    edited_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
                    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                    if regular_editing == 2:
                        edited_frame = crop_the_frame(frame_height, frame_width, edited_frame, regular_editing)
                else:
                    edited_frame = crop_the_frame(frame_height, frame_width, frame, regular_editing)
                    edited_frame = replace_non_white_with_black(edited_frame)
                res = cv2.matchTemplate(edited_frame, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)

                stop_running = False

                # If anything is detected it will show up in zip(*loc[::-1])
                for pt in zip(*loc[::-1]):
                    global nothing_or_something, start, end, exception1, exception2, detections
                    nothing_or_something = 'something'
                    for item in track_frames[-3:]:
                        if item == 'something':
                            stop_running = True
                            break
                    if not stop_running:
                        win_status = [3000, 1500, 700, 200]
                        middle1 = start + 1.5
                        middle2 = start + 2.96666
                        detections += 1
                        time_clip1 = (current_timestamp - win_status[1]) / 1000
                        time_clip2 = (current_timestamp - win_status[2]) / 1000
                        subclip1 = original_clip.subclip((current_timestamp - win_status[0]) / 1000, time_clip1)
                        target_clip = original_clip.subclip(time_clip1, time_clip2)
                        try:
                            subclip2 = original_clip.subclip(time_clip2, (current_timestamp + win_status[3]) / 1000)
                        except:
                            exception1 = True
                        try:
                            audio_clips = audio_clip.subclip(start, middle1)
                            audio_clips2 = audio_clip.subclip(middle1, middle2)
                            if not turn_off_effects:
                                audio_clips2 = audio_clips2.volumex(0.7)
                            audio_clips3 = audio_clip.subclip(middle2, end)
                        except:
                            exception2 = True
                        if not turn_off_effects:
                            target_clip = target_clip.resize(lambda t: 1 + 0.3 * t)
                            target_clip = target_clip.fx(vfx.colorx, 1.5)
                            target_clip = target_clip.speedx(0.6)
                            target_audio = target_clip.audio
                            background_sfx = AudioFileClip(absolute_paths("editing_sfx/bass_boosted_fixed.mp3"))
                            background_sfx = background_sfx.audio_fadeout(0.2)
                            try:
                                adjusted_audio_clip = target_audio.volumex(0.5)
                                combined_audio = CompositeAudioClip([adjusted_audio_clip, background_sfx])
                                target_clip = target_clip.set_audio(combined_audio)
                            except:
                                target_clip = target_clip.set_audio(background_sfx)
                        if not exception2:
                            audio_clips_list.append(audio_clips)
                            audio_clips_list.append(audio_clips2)
                            audio_clips_list.append(audio_clips3)
                        clips_list.append(subclip1)
                        clips_list.append(target_clip)
                        if not exception1:
                            clips_list.append(subclip2)
                        start = start + 3.86666
                        end = end + 3.86666

                    detection_already_found = True
                    break

        def watch_screen():
            results = model(frame)[0]
            stop_running = False

            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result
                class_name = results.names[int(class_id)].lower()
                if (score > threshold) and ('kill' in class_name or class_name == '0'):
                    global nothing_or_something, start, end, exception1, exception2, detections
                    if which_game == 'Minecraft (PVP server)':
                        detections += 1
                        clips_list.append(
                            original_clip.subclip(current_timestamp / 1000, (current_timestamp + 1000) / 1000))
                        try:
                            cap.set(cv2.CAP_PROP_POS_MSEC, current_timestamp + 1000)
                        except:
                            pass
                    else:
                        nothing_or_something = 'something'
                        for item in track_frames[-25:]:
                            if item == 'something':
                                stop_running = True
                                break
                        if not stop_running:
                            win_status = [2000, 1000, 200, 600]
                            middle1 = start + 1.5
                            middle2 = start + 2.96666
                            if class_name == '':  # round_end
                                win_status = [3000, 3000, 2000, 200]
                                middle1 = start + 0
                                middle2 = start + 2.16666
                                detections += 1
                            else:
                                detections += 1
                            time_clip1 = (current_timestamp - win_status[1]) / 1000
                            time_clip2 = (current_timestamp - win_status[2]) / 1000
                            subclip1 = original_clip.subclip((current_timestamp - win_status[0]) / 1000, time_clip1)
                            target_clip = original_clip.subclip(time_clip1, time_clip2)

                            try:
                                subclip2 = original_clip.subclip(time_clip2, (current_timestamp + win_status[3]) / 1000)
                            except:
                                exception1 = True
                            try:
                                audio_clips = audio_clip.subclip(start, middle1)
                                audio_clips2 = audio_clip.subclip(middle1, middle2)
                                if not turn_off_effects:
                                    audio_clips2 = audio_clips2.volumex(0.7)
                                audio_clips3 = audio_clip.subclip(middle2, end)
                            except:
                                exception2 = True
                            if not turn_off_effects:
                                target_clip = target_clip.resize(lambda t: 1 + 0.3 * t)
                                target_clip = target_clip.fx(vfx.colorx, 1.5)
                                target_clip = target_clip.speedx(0.6)
                                target_audio = target_clip.audio
                                adjusted_audio_clip = target_audio.volumex(0.5)
                                background_sfx = AudioFileClip(absolute_paths("editing_sfx/bass_boosted_fixed.mp3"))
                                background_sfx = background_sfx.audio_fadeout(0.2)
                                combined_audio = CompositeAudioClip([adjusted_audio_clip, background_sfx])
                                target_clip = target_clip.set_audio(combined_audio)
                            if not exception2:
                                audio_clips_list.append(audio_clips)
                                audio_clips_list.append(audio_clips2)
                                audio_clips_list.append(audio_clips3)
                            clips_list.append(subclip1)
                            clips_list.append(target_clip)
                            if not exception1:
                                clips_list.append(subclip2)
                            start = start + 3.86666
                            end = end + 3.86666
                    break

        if read_screen_bool:
            read_screen()
        else:
            watch_screen()
        track_frames.append(nothing_or_something)
        for _ in range(1, amount_frames_to_skip):
            ret, frame = cap.read()
            if not ret:
                break

    cap.release()
    cv2.destroyAllWindows()

    try:
        final_clip = concatenate_videoclips(clips_list, method="compose")
        if which_game == 'Minecraft (PVP server)' or turn_off_effects:
            while audio_clip.duration < final_clip.duration:
                audio_clip = concatenate_audioclips([audio_clip, audio_clip])
            if not turn_off_effects:
                final_clip = final_clip.fadeout(0.4)
            audio_clip = audio_clip.volumex(music_volume)  # TODO: user should be able to adjust this 1
            audio_clip = audio_clip.subclip(0, final_clip.duration)
            combined_audio2 = CompositeAudioClip([final_clip.audio, audio_clip])
            if not turn_off_effects:
                combined_audio2 = combined_audio2.audio_fadeout(0.4)
            final_clip = final_clip.set_audio(combined_audio2)
        else:
            concatenated_audio = concatenate_audioclips(audio_clips_list)
            while concatenated_audio.duration < final_clip.duration:
                concatenated_audio = concatenate_audioclips([concatenated_audio, concatenated_audio])
            audio_clip = concatenated_audio.volumex(music_volume)  # TODO: user should be able to adjust this 1
            audio_clip = audio_clip.subclip(0, final_clip.duration)
            combined_audio2 = CompositeAudioClip([final_clip.audio, audio_clip])
            combined_audio2 = combined_audio2.audio_fadeout(0.4)
            final_clip = final_clip.set_audio(combined_audio2)
            if not turn_off_effects:
                final_clip = final_clip.fadeout(0.4)
        if not no_intro_text and which_game != 'Minecraft (PVP server)':
            intro_clip = create_intro_text_clip(args[7], frame_width, frame_height)
            a3 = AudioFileClip(music_choice)
            if a3.duration >= intro_clip.duration:
                a3 = a3.subclip(0, intro_clip.duration)
                a3 = a3.volumex(music_volume)
            intro_clip = intro_clip.set_audio(a3)
            final_clip = concatenate_videoclips([intro_clip, final_clip])
        editing_eta = str((((detections * 16) / 60) * frame_height) / 1080)[:6]
        if which_game == 'Minecraft (PVP server)':
            editing_eta = str(((detections / 60) * frame_height) / 1080)[:6]
        print(f"\nProgram: Editing your video now. ETA: {editing_eta} minute(s)")
        final_clip.write_videofile(f"{args[1]}/{output_filename}_output.mp4", codec='libx264', audio_codec='aac',
                                   logger=None)
        print(f"Program: All done! The edited video can be found here: {args[1]}/{output_filename}_output.mp4")
    except Exception as e:
        print(e)
        print(f"\nModel: No detections found of the game {which_game} in the selected video.")
