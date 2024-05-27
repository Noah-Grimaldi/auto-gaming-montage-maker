import PySimpleGUI as sg
import subprocess
import os
from PIL import ImageColor
import matplotlib.font_manager as fm
import threading
import shutil
import signal
from packagefiles.video_transcribe_audio import process_arguments
from packagefiles.video_remove_silence import remove_silence_main
from packagefiles.edit_video import auto_game_montage
import multiprocessing

run_next_thread = False
base64_image = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAH+UExURQAAAP87If87If87If87If87If87If87If87If87If87ISUjJFAlIe5sFiUjJCMgIfU5IP87If46IPI5IKszH7lxFf93Fv90Fv9xF+pbGsMzINQ2IaovH62jC//xANnNBZGID6yKEfmAE/d4FL9JG9s2IKaRDvPOA+/FBX5UF89EHe04IF9YFf/wAPjeAe/DBL2VENA/Iek6IH9bFv7wAPvlAcKeC7Z1Eug5IKNlFO3gAv7xAPniAfDTA8N6EYstIMyUDuvdAvPNBJF7EfZcGeE3IPmQEfnsAP7oAfjWAvC3B/C1B/CzCIYrIP49IP63Cv+7Cf++Cf/BCNjMBfvoAO/CBdWkCfxBH6EvH6+lC/faAr6bC/CJELkyIP9IL/5zFsi2B/zpAPTRA+m3C7tQKHVTT/7sAPDFBGtZFftJHvw8I/k6IIpCG9WtCHwtH5k7HczABvzsAO7CBYNsE+BYGbIxILUxIOc4IP6UEcq+B/3tAPjfAvjeAtzHBaOZDZZ7EIpDG/5AH+5IJFk/KzYyHaCWDfrjAfHKA3dEGtw/H+o4IU9JGP3sAOK7BquCENc1IO44IIpYGfvnAfnhAc6RDXEvHn9CHOLVBPTUA6yTDfVzFMw0IGknIOPRBPDJBFw8GuVBHtVaGcilCcKQDMEzIPlnGMGLDYU8HMYzIP///xk1TTUAAAARdFJOUwAMWp+/Hg+PLc/vBoP2ARovY7xO3wAAAAFiS0dEqScPBgQAAAAHdElNRQfnCw0WKRQEGPwCAAABjklEQVQ4y2NggANGJmYWQSBgYWZiZMAErMyCSICZFU2ajV0QDbCzIctzcApiAE4OJHkuuLCQMJzJxYFFXlBEVExcQlJKGlkFG5L5MrJyQCCvoKikrAK0BeIOJPepqslBgLqGphbIpWD/IeS1dUCSunJ6+gaGELeAfIvwv5ExSN7E1MzcAh4ewPBDGGBpJSdnbWNrZ4/kWUYGJjjbwREo7+Ts4oocGkwIG9xMwBa4e3h6efv4IuxggbL8/AMCg4JBSkJCw8LhJrAwIJsXEQlUEBUdE4skBlYQB2HHJ8jJJSYlp6BECZIJqWlAV6RnZGZhV5CdYy1nHZWbhx6pcEfmF8hZFxYVl5SWlSPLs8C8WVEJDISq6prauvoGZAXMsIBqbGpuabWWk2tr7+hEDSh4UHd1y8n19Pb1ozqBER5ZEybqTpo8ZSqaE5kR0T1t+oyZs2aj+4EVnmDmzJ03fwG6NCTBgJPcwkWLl2BIw5IcMNEuXbYcUxqRrLl5eFfgk2fg4xcgkHEIZz3CmRd39gcA0k9l8LbQyIEAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjMtMTEtMTNUMjI6NDE6MjArMDA6MDC1A2E6AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTExLTEzVDIyOjQxOjIwKzAwOjAwxF7ZhgAAACh0RVh0ZGF0ZTp0aW1lc3RhbXAAMjAyMy0xMS0xM1QyMjo0MToyMCswMDowMJNL+FkAAAAASUVORK5CYII='
already_occured = False

if __name__ == '__main__':
    # Pyinstaller fix because ultralytics references differently
    multiprocessing.freeze_support()
    

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def retrieve_default_music():
    file_names = [f for f in os.listdir('default_audio') if os.path.isfile(os.path.join('default_audio', f))]
    file_names.extend(['other', 'none'])
    return file_names


def retrieve_available_fonts():
    system_fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    font_names = [os.path.splitext(os.path.basename(font))[0] for font in system_fonts]
    return font_names


def retrieve_available_colors():
    available_colors = list(ImageColor.colormap.keys())
    return available_colors


sg.theme('Black')
dropdown_options4 = [("center"), ("center", "top"), ("center", "bottom"), ("left", "top"), ("right", "top"),
                     ("left", "bottom"), ("right", "bottom")]
dropdown_options = ["tiny", "base", "small", "medium", "large"]
dropdown_games = ["Fortnite", "MW 2019", "MW Warzone 2019", "MWII 2022", "MWIII 2023", "Apex Legends",
                  "Rainbow Six Siege", "PUBG", "Destiny 2", "Rocket League", "CSGO", "Valorant", "Overwatch",
                  "Minecraft (PVP server)"]
# Define the layout of the GUI
auto_montage_layout = [
    [sg.Text('Choose text for intro clip:', tooltip="If you leave this blank there will be no intro text title"),
     sg.InputText(size=(20, 1), key='title_text', tooltip="If you leave this blank there will be no intro text title")],
    [sg.Text("Which game is this?"),
     sg.Drop(values=dropdown_games, background_color='white', key="which_game", default_value="Fortnite",
             readonly=True, text_color='black',
             tooltip="Choose the game that your video contains.")],
    [sg.Text("Choose montage music"),
     sg.Drop(values=retrieve_default_music(), background_color='white', key="dropdown_audio",
             default_value="Shadows - Anno Domini Beats.mp3",
             readonly=True, text_color='black', size=30,
             tooltip="Choose the audio you want to overlay over your montage"),
     sg.FileBrowse(file_types=(("Audio Files", "*.mp3;*.wav;*.flac;*.ogg"),), visible=False,
                   key='music_choice', tooltip="Supported file types include: *.mp3;*.wav;*.flac;*.ogg")],
    [sg.Text("Edit with video effects:"),
     sg.Drop(values=["yes", "no"], background_color='white', key="effects_bool", default_value="yes",
             readonly=True, text_color='black',
             tooltip="This is selecting if you want video effects in the video or just the highlights, letting you edit yourself.")],
    [sg.Text("Adjust Music Volume (%):",
             tooltip="Volume of the overlayed music from 0-200%"),
     sg.Slider(range=(0, 200), default_value=100, orientation='h', size=(23, 10), trough_color="white",
               border_width=6,
               key='music_volume', tooltip="Volume of the overlayed music from 0-200%")],
    [sg.Text("Make editing faster (frames):\n(forfit precision for speed)",
             tooltip="You can increase model speed by skipping frames in the video, by default this skips by 2 frames\ndepending on your video's FPS, "),
     sg.Slider(range=(2, 100), default_value=2, orientation='h', size=(23, 10), trough_color="white",
               border_width=6,
               key='skip_frames', tooltip="This is in frames, you have the ability to skip 2-625 frames within the video")],
]
auto_captions_layout = [
    [sg.Text("Select model size: \n(smaller the model, quicker the export)"),
     sg.Drop(values=dropdown_options, background_color='white', key="dropdown_option", default_value="tiny",
             readonly=True, text_color='black',
             tooltip="It transcribes your video's audio with a model, by default it is tiny,\nyou can choose a larger model to make it more accurate at the\nexpense of taking longer")],
    [sg.Text("Adjust text color/font/position/size:")],
    [sg.Text("Color:    "),
     sg.Drop(values=retrieve_available_colors(), background_color='white', key="dropdown_option2",
             default_value="white",
             readonly=True, text_color='black',
             tooltip="this is the text color that will overlay\non your edited video")],
    [sg.Text("Font:     "),
     sg.Drop(values=retrieve_available_fonts(), background_color='white', key="dropdown_option3", default_value="arial",
             size=(21, 1),
             readonly=True, text_color='black',
             tooltip="this is the font style for the overlay text")],
    [sg.Text("Position:"),
     sg.Drop(values=dropdown_options4, background_color='white', key="dropdown_option4",
             default_value=("center", "bottom"), size=(21, 1),
             readonly=True, text_color='black',
             tooltip="this is the position for the overlay text")],
    [sg.Text("Text Size:", tooltip="Adjust the size of the output overlay text")],
    [sg.Slider(range=(0, 200), default_value=100, orientation='h', size=(30, 10), trough_color="white",
               border_width=6,
               key='-SIZE-', tooltip="Font size/text size of overlay text")],
]
silence_removal_layout = [
    [sg.Text("Adjust Silence Threshold:",
             tooltip="To remove silence, the program needs to know what\n volume is considered silence in your video, by default it is -50.")],
    [sg.Slider(range=(-100, 100), default_value=-50, orientation='h', size=(30, 10), trough_color="white",
               border_width=6, key='-THRESHOLD-',
               tooltip="To remove silence, the program needs to know what\n volume is considered silence in your video, by default it is -50.")],
]

layout = [
    [sg.InputText(key="video_file", disabled=True, default_text=r"Select one or multiple video file(s) to edit *",
                  tooltip="The video(s) you want to be edited, make sure file names don't have ';' in them",
                  text_color='black'),
     sg.FilesBrowse(file_types=(("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv;*.flv;*.webm"),))],
    [sg.InputText(key="output_folder", default_text=r"Select an output folder", disabled=True,
                  tooltip="The folder where you want the edited video to export", text_color='black'),
     sg.FolderBrowse()],
    [sg.Checkbox("Remove Silent Portions", key="option1",
                 tooltip="If selected, this option will cut out all detected silence from your video"),
     sg.Checkbox("Automatic Captions", key="option2",
                 tooltip="If selected, this option will automatically transcribe your\nvideo audio and place captions for every word on to the edited video")],
    [sg.Checkbox("Automatic Video Game Montage", key="option3",
                 tooltip="If selected, this option will create an automatic video montage from a directory\n full of clips or a video. SUPPORTED GAMES INCLUDE: Fortnite, Apex Legends, Call of Duty,\nRocket League, CSGO, Valorant, Overwatch, or Minecraft PVP.")],
    [sg.pin(sg.Column(silence_removal_layout, key='-ROW1-', visible=False, pad=(0, 0)))],
    [sg.pin(sg.Column(auto_captions_layout, key='-ROW2-', visible=False, pad=(0, 0)))],
    [sg.pin(sg.Column(auto_montage_layout, key='-ROW3-', visible=False, pad=(0, 0)))],
    [sg.Text('Loading . . .', key='loading_text', visible=False, text_color='yellow')],
    [sg.Button("Edit Video", visible=True, button_color=('white', 'green')),
     sg.Button("Cancel", visible=False, button_color=('white', 'darkred'))],
    [sg.Button("Output Folder", visible=False, button_color=('black', 'lightblue'))]
]
# Create the window
window = sg.Window("Automatic Video Editing", layout, icon=base64_image)
# Event loop
while True:
    event, values = window.read(timeout=200)
    if event == sg.WINDOW_CLOSED:
        if os.path.isdir("output_images"):
            shutil.rmtree("output_images")
        if os.path.exists("output_audio.wav"):
            os.remove("output_audio.wav")
        break
    if len(values['title_text']) > 12 and not already_occured:
        already_occured = True
        sg.popup('This textbox only accepts 12 characters even if you type more.', title='Warning')
    if values["option1"]:
        window['-ROW1-'].update(visible=True)
    else:
        window['-ROW1-'].update(visible=False)
    if values["option2"]:
        window['-ROW2-'].update(visible=True)
    else:
        window['-ROW2-'].update(visible=False)
    if values["option3"]:
        window['option1'].update(disabled=True)
        window['option2'].update(disabled=True)
        window['-ROW3-'].update(visible=True)
        if values['dropdown_audio'] == 'other':
            window['music_choice'].update(visible=True)
        else:
            window['music_choice'].update(visible=False)
        try:
            window['-ROW2-'].update(visible=False)
            window['-ROW1-'].update(visible=False)
        except:
            pass
    else:
        window['-ROW3-'].update(visible=False)
        window['option1'].update(disabled=False)
        window['option2'].update(disabled=False)
    try:
        if not run_thread.is_alive():
            filename1, extension1 = os.path.basename(values["video_file"]).split('.')
            new_filename = f"{filename1}_output.mp4"
            dualProcessFilePath = output2 + '/' + new_filename
            if run_next_thread:
                next_thread = threading.Thread(target=remove_silence_main,
                                               args=(dualProcessFilePath, output2, str(values["-THRESHOLD-"])))
                next_thread.start()
                next_thread.join()
                run_next_thread = False
                os.remove(dualProcessFilePath)
            window['Edit Video'].update(visible=True)
            window['Cancel'].update(visible=False)
            window['loading_text'].update(visible=False)
            window['Output Folder'].update(visible=True)
            shutil.rmtree("output_images")
            os.remove("output_audio.wav")
    except:
        pass
    if event == "Output Folder":
        if values["output_folder"] == 'Select an output folder':
            if ';' in values["video_file"]:
                output1 = os.path.dirname(values["video_file"].split(';')[0])
            else:
                output1 = os.path.dirname(values["video_file"])
        else:
            output1 = values["output_folder"]
        path_with_backslashes = output1.replace('/', '\\')
        subprocess.Popen(['explorer', path_with_backslashes])
    if event == "Cancel":
        if os.path.isdir("output_images"):
            shutil.rmtree("output_images")
        os.kill(os.getpid(), signal.SIGINT)
    elif event == "Edit Video":
        if values["output_folder"] == 'Select an output folder':
            if ';' in values["video_file"]:
                first_path = values["video_file"].split(';')[0]
            else:
                first_path = values["video_file"]
            output2 = os.path.dirname(first_path)
        else:
            output2 = values["output_folder"]
        if values["video_file"] == "Select one or multiple video file(s) to edit *" or (
                not values["option1"] and not values["option2"] and not values["option3"]) or values[
            'dropdown_audio'] == 'other':
            sg.popup("Please select a video file, music file, or editing style.", title="Error", icon="ERROR")
        else:
            if values["option3"]:
                try:
                    cls()
                    run_thread = threading.Thread(target=auto_game_montage, args=(
                        values["video_file"], output2, values['dropdown_audio'], values['music_volume'],
                        values['which_game'], int(values['skip_frames']), values['effects_bool'], values['title_text'][:12]))
                    run_thread.start()
                except Exception as e:
                    sg.popup(e, title="No highlights detected", icon="ERROR")
            else:
                if values["option1"] and values["option2"]:
                    try:
                        cls()
                        run_thread = threading.Thread(
                            target=process_arguments,
                            args=(
                                values["video_file"], "True", output2, values["dropdown_option"],
                                values["dropdown_option2"],
                                values["dropdown_option3"], f'{values["dropdown_option4"]}', str(values["-SIZE-"])))
                        run_thread.start()
                        run_next_thread = True
                    except Exception as e:
                        sg.popup(e, title="Error", icon="ERROR")
                else:
                    if values["option1"]:
                        try:
                            cls()
                            run_thread = threading.Thread(target=remove_silence_main,
                                                          args=(
                                                              values["video_file"], output2,
                                                              str(values["-THRESHOLD-"])))
                            run_thread.start()
                        except Exception as e:
                            sg.popup(e, title="Error", icon="ERROR")
                    else:
                        if values["option2"]:
                            try:
                                cls()
                                run_thread = threading.Thread(
                                    target=process_arguments,
                                    args=(values["video_file"], "True", output2, values["dropdown_option"],
                                          values["dropdown_option2"],
                                          values["dropdown_option3"], f'{values["dropdown_option4"]}',
                                          str(values["-SIZE-"])))
                                run_thread.start()
                            except Exception as e:
                                sg.popup(e, title="Error", icon="ERROR")
            window['Output Folder'].update(visible=False)
            window['Edit Video'].update(visible=False)
            window['Cancel'].update(visible=True)
            window['loading_text'].update(visible=True)
window.close()
