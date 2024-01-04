# `Automatic Video Editing` (auto-game-montage, auto-silence-removal, and auto-captions)

This is a tool for editors that automatically edits video game montages based off eliminations, knocks, wins, or punches. It can also remove silent portions and add automatic captions to your video file with a simple GUI.

# `FOR REGULAR USAGE`

## Demo for Silent Portions and Automatic Captions
![](example.gif)

# `FOR DEVELOPER USAGE`

Run editorGUI.py, which programmatically references the other files or [download the EXE](https://github.com/Noah-Grimaldi/automatic-video-editing/releases/download/pyinstaller/automatic-video-editing.exe) (The EXE is currently only for Windows).

**If you want to run the argparse files individually:**

For [video-remove-silence](packagefiles/video-remove-silence.py): 

adjust_silence_threshold is the decibal threshold that video-remove-silence considers as "silence." (avg. -40 or -50)

For [video_transcribe_audio.py](packagefiles/video_transcribe_audio.py): 

model_size can be tiny, base, small, medium, large; text_color (e.g. white); font (e.g. Arial-Black or ''); position (e.g. ('center', 'bottom')); text_size (e.g. 80.0)

## Dependencies
`pip install -r requirements.txt`
- Python 3.5+ download(s): [Windows](https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe)/[Mac](https://www.python.org/ftp/python/3.12.0/python-3.12.0-macos11.pkg)/[Linux](https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tar.xz)
- FFmpeg download(s): [Windows](https://community.chocolatey.org/packages/ffmpeg)/[Mac](https://formulae.brew.sh/formula/ffmpeg)/[Linux](https://www.geeksforgeeks.org/how-to-install-ffmpeg-in-linux/)

## Platform Support 
Windows/Mac/Linux

## Credits
Credit to @excitoon for [video-remove-silence](https://github.com/excitoon/video-remove-silence)

