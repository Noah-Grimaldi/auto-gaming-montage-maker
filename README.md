# `Automatic Video Editing` (auto-game-montage, auto-silence-removal, and auto-captions)

This is a tool for editors that automatically edits video game videos/clips pertaining to Fortnite, Apex Legends, Valorant, Call Of Duty, Overwatch, Minecraft, Rainbow Six Siege, Destiny 2, PUBG, and Rocket League in order to make them into montages based off eliminations, knocks, wins, goals, or punches. It can also remove silent portions and add automatic captions to your video file with a simple GUI.

# `FOR REGULAR USAGE:`

## Simple Instruction
**Windows:**
- Download the installer [here](https://github.com/Noah-Grimaldi/auto-gaming-montage-maker/releases/download/v1.0.0/agmsetupwin.exe)
- Run the installer
  
**MAC:**
- Download the zip folder [here](https://github.com/Noah-Grimaldi/auto-gaming-montage-maker/releases/download/v1.0.0/agmsetupmacos.zip)
- Double-click to uncompress the folder, and go into the uncompressed folder
- Bypass the "Unidentified Developer" Warning
- Right-click or control-click the "editor_gui" unix executable file and hit open, then confirm open.
- It should install Homebrew and FFMPEG if you don't have them on your system.

**Linux:**
- Download the compressed agmsetuplinux.tar.gz folder [here](https://drive.google.com/file/d/1EBKRwK3fVsPy5I71j_wzTSI35GjahjyB/view?usp=sharing).
- Then navigate to where you downloaded it and uncompress it with this command:
`tar -xzvf agmsetuplinux.tar.gz`
- Navigate inside the uncompressed directory and run these commands to run the executable:
`chmod +x editor_gui`
`./editor_gui`

## Examples/Tutorial
- [Tutorial](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp)
- [Fortnite Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=315)
- [Valorant Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=709)
- [Apex Legends Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=454)
- [Rocket League Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=699)
- [MW3 Gun-game Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=542)
- [MW3 FFA Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=485)
- [MW3 Kill Confirmed Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=268)
- [Warzone Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=188)
- [CSGO Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=215)
- [Minecraft Example](https://youtu.be/mjZggkEld50?si=kVlOT_8-KW_prgbp&t=607)

## What specific video edits does the program do?
- The program changes brightness, turns down audio volume, zooms, adds a bass boosted sound effect ([here](editing_sfx/bass_boosted_fixed.mp3)) for about 3 seconds on all highlights.
- Exceptions: Minecraft does no special effects, but merely captures the hit registers on other players.

## What games does it edit?
- The automatic montage maker edits video game videos/clips
- Games it can interpret: Fortnite, Apex Legends, MW3 Gun-game, MW3 kill-confirmed, MW3 free-for-all, Warzone 2.0+, Rocket League, CSGO, Valorant, Overwatch, Rainbow Six Siege, Destiny 2, PUBG, and Minecraft (PVP Servers).

## Acceptable audio/video types
- audio types: mp3, wav, flac, ogg
- video types: mp4, avi, mkv, mov, wmv, flv, webm

## Demo for Auto Gaming Montages
![](montagedemo.gif)
## Demo for Silent Portions and Automatic Captions
![](example.gif)

# `FOR DEVELOPER USAGE:`

Clone the repository with --recurse-submodules so PySimpleGUI's older version will be included:

`git clone --recurse-submodules https://github.com/Noah-Grimaldi/auto-gaming-montage-maker.git`

Run editor_gui.py, which programmatically references the other files or [download Windows or MAC executables](https://github.com/Noah-Grimaldi/auto-gaming-montage-maker/releases/tag/v1.0.0).

## Table for different game's model speed and accuracy rating
|                                 | CSGO Model    | Minecraft Model | Overwatch Model | Valorant Model | Other games (template matching) |
| ------------------------------- | ------------- | --------------- | --------------- | -------------- | ------------------------------- |
| Average Speed (On 1 minute clip)| 35 seconds    | 25 seconds      | 1 minute        | 35 seconds     | 55 seconds                      |
| Accuracy (1-5 rating)           | 5             | 3               | 3               | 5              | 5 (Besides R6, which is a 3)    |

## How does the program edit the games?
- The model looks at wins, eliminations, and/or knocks for all games except Rocket League and Minecraft.
- For Rocket League, the model watches for goals (sometimes wins).
- For Minecraft, the model watches for hits on other players.
- Fortnite, Apex Legends, COD games, Rainbow Six Siege, Destiny 2, PUBG, and Rocket League use template matching to see if there was actually a highlight.
- The program treats each highlight as a 3.2 second clip, I may end up adding a different feature where it doesn't just do montage format but full on video editing.

## Roboflow datasets I used or created
**Already created datasets:**
- [Minecraft Dataset](https://universe.roboflow.com/benjamin-t1dqd/minecraft-pvp-ai/browse?queryText=class%3APlayer&pageSize=200&startingIndex=0&browseQuery=true)
- [Valorant Dataset](https://universe.roboflow.com/suman-kumar-dx18l/valorant-kill-banner-woebs/images/ZGUdwP6PpO7qMgHOXWh0?queryText=&pageSize=50&startingIndex=50&browseQuery=true)

**Datasets I created:**
- [CSGO Dataset](https://universe.roboflow.com/overwatchkillsign/csgo-head-and-kill)
- [Overwatch Dataset](https://universe.roboflow.com/overwatchkillsign/overwatch-kill-sign-detector)
- [Fortnite, Apex, COD, Rocket League Dataset](https://universe.roboflow.com/overwatchkillsign/fortnite-apex-league-cod) (no longer using this one, but if you'd like to improve it and use it, you can)

## Facilitated Testing
If you need to have test video examples from Youtube, [this](https://github.com/ytdl-org/youtube-dl) is a great tool on Github for obtaining the videos to use in your program for testing. 

After writing this I'm looking into the legality of this tool and I'm not 100% sure the youtube-dl is legal, although it is a larger open source community project that has been on Github for over 3 years now, so I'm assuming it would have been taken down at this point if it were not (I could be wrong, this is just a heads up).

## Options explained for threaded methods
For [edit_video.py](packagefiles/edit_video.py): 

- *video_file*: path to video selected video file
- *output2*: path to selected video output 
- *dropdown_audio*: the default_audio directory, other (any music of your choice), and none.
- *title_text*: True or False, (leave input blank for no intro clip)
- *which_game*: CSGO, MW3 gun game, MW3 kill confirmed, MW3 free-for-all, Fortnite, Apex Legends, Valorant, Overwatch, Warzone 2.0+, Rocket League, Minecraft (PVP Server).
- *music_volume*: 0-200% adjustment for chosen music, or nothing if "none" selected.
- *skip_frames*: 2-100 frames ability to adjust in order to have cv2 skip through the video faster with less precision. (skipping frames only works for Minecrafft, Overwatch, CSGO, and Valorant)
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
- Windows Instruction: [Download Python 3.10](https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe), then download [FFMPEG](https://community.chocolatey.org/packages/ffmpeg).
- MAC Instruction: Install [Homebrew](https://brew.sh/), then if you already have python 3.10 downloaded, uninstall it.
  
  First do `brew install python-tk@3.10`
  
  Then do `brew install python@3.10`
  
  Then install FFMPEG `brew install ffmpeg`
  
- Linux Instruction: Install [Python 3.10](https://www.knowledgehut.com/blog/data-science/install-python-on-ubuntu) and [FFMPEG](https://phoenixnap.com/kb/install-ffmpeg-ubuntu) You may also need to install python3.10-tk:

  `sudo apt-get install python3.10-tk`

**After** you've activated the venv on your specified platform, run the command: `pip install -r requirements.txt`

## Platform Support 
Windows/Mac/Linux

## Credits
Credit to @excitoon for [video-remove-silence](https://github.com/excitoon/video-remove-silence)

