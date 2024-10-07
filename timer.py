# go through subdirectories and find all the files with the extension .mp3/m4b
# go through multiple levels of subdirectories to account for book series
# calculate length of each file and add it to a total time
import os
import datetime
from mutagen.mp3 import MP3
import math

def get_directories(path):
    items = os.listdir(path)
    # filter out only directories
    directories = []
    for item in items:
        if os.path.isdir(os.path.join(path, item)):
            directories.append(item)
    # add path
    directories = [os.path.join(path, item) for item in directories]
    return directories

def get_media_files(path):
    items = os.listdir(path)
    # filter out only mp3 files (add m4b later)
    media_files = [item for item in items if item.endswith('.mp3')]
    # add path
    media_files = [os.path.join(path, item) for item in media_files]
    return media_files

def get_mp3_length(file):
    audio = MP3(file)
    return audio.info.length

def get_total_length(files):
    return sum([get_mp3_length(file) for file in files])

def seconds_to_hms(seconds):
    delta = datetime.timedelta(seconds=math.floor(seconds))
    return str(delta)

#path = "c:\\Users\\juraj\\OneDrive\\media\\audiobooks\\František Kotleta\\František Kotleta - Lovci"
path = "c:\\Users\\juraj\\OneDrive\\media\\audiobooks\\František Kotleta\\František Kotleta - Bratrstvo krve"
dirs = get_directories(path)
print(dirs)
for dir in dirs:
    files = get_media_files(dir)
    audio_length = get_total_length(files)
    print(dir)
    print(seconds_to_hms(audio_length))