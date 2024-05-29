import platform
import subprocess
import os

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

def install_homebrew():
    try:
        subprocess.run(
            '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
            check=True,
            shell=True
        )
        print("Homebrew installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install Homebrew.")
        exit(1)

def install_ffmpeg():
    try:
        subprocess.run(["brew", "install", "ffmpeg"], check=True)
        print("FFmpeg installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install FFmpeg.")
        exit(1)

def main():
    if is_macos():
        print("You are on macOS.")
        
        if not is_homebrew_installed():
            print("Homebrew is not installed. Installing Homebrew...")
            install_homebrew()
        else:
            print("Homebrew is already installed.")
        
        if not is_ffmpeg_installed():
            print("FFmpeg is not installed. Installing FFmpeg...")
            install_ffmpeg()
        else:
            print("FFmpeg is already installed.")
    else:
        print("You are not on macOS.")
