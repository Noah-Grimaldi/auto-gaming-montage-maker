import cv2
from PIL import Image
import pytesseract
import os

from ultralytics import YOLO
from moviepy.video.fx import all as vfx
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_audioclips
from moviepy.video.compositing.concatenate import concatenate_videoclips

nothing_or_something = 'nothing'
start = 0
end = 3.86666
exception1 = False
exception2 = False
read_screen_bool = True


# arguments include: video_location, output_location, audio_choice, music_volume, which_game
def auto_game_montage(*args):
    which_game = args[4]  # "Fortnite", "MW3 gun-game", "MW3 kill-confirmed", "MW3 free-for-all", "Warzone 2.0+", "Apex Legends", "Rocket League", "CSGO", "Valorant", "Overwatch", "Minecraft (PVP server)"

    model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')
    model = YOLO(model_path)
    threshold = 0.5

    # relative path to pytesseract.exe
    pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR\tesseract.exe'

    cap = cv2.VideoCapture(r'C:\Users\bepan\Downloads\valorantKILLStest.mp4')  # TODO: user should be able to adjust this 1
    cap.set(cv2.CAP_PROP_POS_MSEC, 3000)  # start at 3 seconds due to hardcoded edits
    ret, frame = cap.read()
    track_frames = []
    clips_list = []
    audio_clips_list = []

    keywords = []

    if which_game == 'Fortnite':
        keywords = ["victory", "ovale", "eliminated", "knocked"]
    elif which_game == 'Apex Legends':
        keywords = ["eliminated", "knocked", "champion"]
    elif which_game == 'MW3 gun-game':
        keywords = ["victory", "gun promotion"]
    elif which_game == 'MW3 kill-confirmed' or which_game == 'MW3 free-for-all':
        keywords = ["victory", "one shot, one kill", "2nd kill", "1st kill", "3rd kill", "revenge", "jumpshot",
                    "buzzkill", "grounded", "kingslayer", "th ki", "tripl", "double kill", "quad feed",
                    "longshot",
                    "point blank", "survivor", "bloodthirsty"]
    elif which_game == 'Warzone 2.0+':
        keywords = ["victory", "enemy downed", "gulag winner"]
    elif which_game == 'Rocket League':
        keywords = ["scor"]
    else:
        global read_screen_bool
        read_screen_bool = False

    original_clip = VideoFileClip(
        r'C:\Users\bepan\Downloads\valorantKILLStest.mp4')  # TODO: user should be able to adjust this 1
    audio_clip = AudioFileClip('./default_audio/Same Time - Spence.mp3')  # TODO: user should be able to adjust this 1
    while ret:  # iterating through the video frames and skipping 1 every iteration
        current_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)

        print(current_timestamp)
        global nothing_or_something, exception1, exception2
        exception1 = False
        exception2 = False
        nothing_or_something = 'nothing'

        def read_screen():

            def crop_bottom_middle(frame):  # this crops each frame to the middle to ignore the chat log
                H, W, _ = frame.shape
                bottom_middle_region = frame[:, W // 4: 3 * W // 4]
                if which_game == 'Warzone 2.0+':
                    bottom_middle_region = frame[:, W // 5: 3 * W][:H - 300, :]
                return bottom_middle_region

            bottom_middle_frame = crop_bottom_middle(frame)
            pillow_convert = Image.fromarray(bottom_middle_frame)
            text = pytesseract.image_to_string(pillow_convert, lang='eng', config='--psm 6')

            stop_running = False
            if any(keyword in text.lower() for keyword in keywords):
                global nothing_or_something, start, end, exception1, exception2
                nothing_or_something = 'something'
                if which_game == "Warzone 2.0+" and 'victory' in text.lower():
                    lookback = -36
                else:
                    lookback = -25
                if which_game == "Rocket League" and '+' not in text.lower():  # make this "not in text.lower"
                    stop_running = True
                for item in track_frames[lookback:]:
                    if item == 'something':
                        stop_running = True
                        break
                if not stop_running:
                    win_status = [3000, 1500, 700, 200]
                    middle1 = start + 1.5
                    middle2 = start + 2.96666
                    if 'ovale' in text.lower() or 'victory' in text.lower() or 'champion' in text.lower():
                        win_status = [3000, 3000, 2000, 200]
                        if which_game == "Warzone 2.0+":
                            win_status = [6000, 6000, 5000, -2000]
                        middle1 = start + 0
                        middle2 = start + 2.16666
                        print(f"WIN at: {current_timestamp}")
                    else:
                        print(f"ELIM or KNOCK at: {current_timestamp}")
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
                        audio_clips2 = audio_clips2.volumex(0.7)
                        audio_clips3 = audio_clip.subclip(middle2, end)
                    except:
                        exception2 = True
                    target_clip = target_clip.resize(lambda t: 1 + 0.3 * t)
                    target_clip = target_clip.fx(vfx.colorx, 1.5)
                    target_clip = target_clip.speedx(0.6)
                    target_audio = target_clip.audio
                    adjusted_audio_clip = target_audio.volumex(0.5)
                    background_sfx = AudioFileClip('../default_audio/bass_boosted_fixed.mp3')
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

        def watch_screen():
            results = model(frame)[0]
            stop_running = False

            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result
                class_name = results.names[int(class_id)].lower()
                print(class_name)
                if (score > threshold) and ('kill' in class_name):
                    global nothing_or_something, start, end, exception1, exception2
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
                            print(f"WIN at: {current_timestamp}")
                        elif 'kill' in class_name:
                            print(f"ELIM or KNOCK at: {current_timestamp}")
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
                            audio_clips2 = audio_clips2.volumex(0.7)
                            audio_clips3 = audio_clip.subclip(middle2, end)
                        except:
                            exception2 = True
                        target_clip = target_clip.resize(lambda t: 1 + 0.3 * t)
                        target_clip = target_clip.fx(vfx.colorx, 1.5)
                        target_clip = target_clip.speedx(0.6)
                        target_audio = target_clip.audio
                        adjusted_audio_clip = target_audio.volumex(0.5)
                        background_sfx = AudioFileClip('./default_audio/bass_boosted_fixed.mp3')
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
                    print('HELLLO')
                    break


        if read_screen_bool:
            read_screen()
        else:
            watch_screen()
        track_frames.append(nothing_or_something)
        ret, frame = cap.read()
        ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    concatenated_audio = concatenate_audioclips(audio_clips_list)
    final_clip = concatenate_videoclips(clips_list, method="compose")
    while concatenated_audio.duration < final_clip.duration:
        concatenated_audio = concatenate_audioclips([concatenated_audio, concatenated_audio])
    final_clip = final_clip.fadeout(0.4)
    audio_clip = concatenated_audio.volumex(0.3)  # TODO: user should be able to adjust this 1
    audio_clip = audio_clip.subclip(0, final_clip.duration)
    combined_audio2 = CompositeAudioClip([final_clip.audio, audio_clip])
    combined_audio2 = combined_audio2.audio_fadeout(0.4)
    final_clip = final_clip.set_audio(combined_audio2)
    final_clip.write_videofile('./output_video.mp4', codec='libx264', audio_codec='aac')


auto_game_montage(0, 1, 2, 3, 'Valorant')
