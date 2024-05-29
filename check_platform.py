import platform
import subprocess


def is_macos():
    return platform.system() == "Darwin"


def is_homebrew_installed():
    try:
        subprocess.run(["brew", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    if is_macos():
        print("You are on macOS.")

        if is_homebrew_installed():
            print("Homebrew is installed.")

            if is_ffmpeg_installed():
                print("FFmpeg is installed.")
            else:
                print("FFmpeg is not installed.")
        else:
            print("Homebrew is not installed.")
    else:
        print("You are not on macOS.")
