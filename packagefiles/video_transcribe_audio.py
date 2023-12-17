import os
import re
import ast
import logging

from PIL import Image, ImageDraw, ImageFont
from faster_whisper import WhisperModel
from moviepy.editor import VideoFileClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

logging.disable(logging.CRITICAL)


def process_arguments(*args):
    def create_text_image(text, output_path, fontstyle, fontsize, text_color):
        image_width = 600
        image_height = 300
        img = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        font_settings = ImageFont.truetype(fontstyle, fontsize)
        bbox = draw.textbbox((0, 0), text, font=font_settings)
        x = (image_width - (bbox[2] - bbox[0])) // 2
        y = (image_height - (bbox[3] - bbox[1])) // 2
        draw.text((x, y), text, fill=text_color, font=font_settings)
        img.save(output_path)

    outputFolder = args[2]
    if args[1]:
        if args[2] == 'Select an output folder':
            outputFolder = ''
        else:
            outputFolder += '/'

        def convert_video_to_audio(video_path, audio_path):
            video = VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(audio_path, logger=None, )
            audio.close()

        video_file_path = args[0]
        video_clip = VideoFileClip(video_file_path)
        audio_file_path = 'output_audio.wav'
        convert_video_to_audio(video_file_path, audio_file_path)
        model_size = args[3]
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_file_path, beam_size=5, word_timestamps=True)
        os.makedirs("output_images", exist_ok=True)
        text_clips = []
        for inner_list in info.word_info:
            for word in inner_list:
                start_time = word.start
                end_time = word.end
                word_text = re.sub(r'\W+', '', word.word)
                text_image_path = f"output_images/{word_text}.png"
                create_text_image(word_text, text_image_path, args[5], float(args[7]), args[4])
                image_clip = ImageClip(text_image_path, duration=end_time - start_time)
                text_clip = image_clip.set_start(start_time).set_end(end_time).set_position(
                    ast.literal_eval(args[6]))
                text_clips.append(text_clip)
        # Composite the video with the text clips
        video_with_text = CompositeVideoClip([video_clip] + text_clips)
        # default video path name for output of export
        file_name = os.path.basename(video_file_path)
        file_name_without_extension = os.path.splitext(file_name)[0]
        # Export the final video
        video_with_text.write_videofile(f"{outputFolder}{file_name_without_extension}_output.mp4", codec='libx264',
                                        logger=None,
                                        fps=video_clip.fps)
