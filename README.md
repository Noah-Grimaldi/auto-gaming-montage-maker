# `Automatic Video Editing` (auto-game-montage, auto-silence-removal, and auto-captions)

This is a tool for editors that automatically edits video game videos/clips to make them into montages based off eliminations, knocks, wins, goals, or punches. It can also remove silent portions and add automatic captions to your video file with a simple GUI.

# `FOR REGULAR USAGE:`

## Simple Instruction
- Download the installer here
- Run the installer 

## What specific video edits does the program do?
- The program changes brightness, turns down audio volume, zooms, adds a bass boosted sound effect ([here](editing_sfx/bass_boosted_fixed.mp3)) for about 3 seconds on all highlights.
- Exceptions: Minecraft does no special effects, but merely captures the hit registers on other players. 
## What does it edit and how?
- The automatic montage maker edits video game videos/clips
- Games it can interpret: Fortnite, Apex Legends, MW3 Gun-game, MW3 kill-confirmed, MW3 free-for-all, Warzone 2.0+, Rocket League, CSGO, Valorant, Overwatch, and Minecraft (PVP Servers).
- The model looks at wins, eliminations, and/or knocks for all games except Rocket League and Minecraft.
- For Rocket League, the model watches for goals (sometimes wins).
- For Minecraft, the model watches for hits on other players.
## Table for different game's model speed and accuracy

## Demo for auto gaming montage

## Demo for Silent Portions and Automatic Captions
![](example.gif)

# `FOR DEVELOPER USAGE:`

Run editorGUI.py, which programmatically references the other files or [download the EXE](https://github.com/Noah-Grimaldi/automatic-video-editing/releases/download/pyinstaller/automatic-video-editing.exe) (The EXE is currently only for Windows).

**What is seen as "highlights?"**

**Options explained for threaded methods:**

For [editVideo.py](packagefiles/editVideo.py): 

- *video_file*: path to video selected video file
- *output2*: path to selected video output 
- *dropdown_audio*: the default_audio directory, other (any music of your choice), and none.
- *title_text*: True or False, (leave input blank for no intro clip)
- *which_game*: CSGO, MW3 gun game, MW3 kill confirmed, MW3 free-for-all, Fortnite, Apex Legends, Valorant, Overwatch, Warzone 2.0+, Rocket League, Minecraft (PVP Server).
- *music_volume*: 0-200% adjustment for chosen music, or nothing if "none" selected.
- *skip_frames*: 2-100 frames ability to adjust in order to have cv2 skip through the video faster with less precision.
- *effects_bool*: 'yes' or 'no' dropdown which can turn off or on video editing effects not including intro clip

For [video-remove-silence](packagefiles/video_remove_silence.py):

- *video_file*: path to video selected video file
- *output2*: path to selected video output
- *-THRESHOLD-*: the decibal threshold that video-remove-silence considers as "silence." (avg. -40 or -50)

For [video_transcribe_audio.py](packagefiles/video_transcribe_audio.py):

- *video_file*: path to video selected video file
- *output2*: path to selected video output
- *dropdown_option*: WhisperAI model for tiny, base, small, medium, or large.
- *dropdown_option2*: text color (e.g. white)
- *dropdown_option3*: font (e.g. Arial-Black or '')
- *dropdown_option4*: position (e.g. ('center', 'bottom'))
- *-SIZE-*: text size (e.g. 80.0)

## Dependencies
`pip install -r requirements.txt`
- Python 3.5+ download(s): [Windows](https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe)/[Mac](https://www.python.org/ftp/python/3.12.0/python-3.12.0-macos11.pkg)/[Linux](https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tar.xz) or [More Options](https://www.python.org/downloads/)
- FFmpeg download(s): [Windows](https://community.chocolatey.org/packages/ffmpeg)/[Mac](https://formulae.brew.sh/formula/ffmpeg)/[Linux](https://www.geeksforgeeks.org/how-to-install-ffmpeg-in-linux/) or [More Options](https://www.ffmpeg.org/download.html)
- Google Tesseract OCR download(s): [Windows](https://github.com/tesseract-ocr/tesseract?tab=readme-ov-file#installing-tesseract)/[Mac](https://formulae.brew.sh/formula/tesseract)/[Linux](https://tesseract-ocr.github.io/tessdoc/Installation.html) or [More Options](https://tesseract-ocr.github.io/tessdoc/Installation.html)

## Platform Support 
Windows/Mac/Linux

## Credits
Credit to @excitoon for [video-remove-silence](https://github.com/excitoon/video-remove-silence)

