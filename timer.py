# go through subdirectories and find all the files with the extension .mp3/m4b
# go through multiple levels of subdirectories to account for book series
# calculate length of each file and add it to a total time
import os
import datetime
import sys
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import math
from tinytag import TinyTag

use_opus = False
output_markdown = True
output = []

def get_directories(path):
    items = os.listdir(path)
    # filter out only directories
    directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
    # add path
    directories = [os.path.join(path, item) for item in directories]
    return directories

def is_media(path):
    if use_opus:
        return path.endswith('.mp3') or path.endswith('.m4b') or path.endswith('.opus')
    else:
        return path.endswith('.mp3') or path.endswith('.m4b')

def get_media_files(path):
    items = os.listdir(path)
    # filter out only mp3 and m4b files
    media_files = [item for item in items if is_media(item)]
    # add path
    media_files = [os.path.join(path, item) for item in media_files]
    return media_files

def get_mp3_length(file):
    if not file.endswith('.mp3'):
        return 0
    audio = MP3(file)
    return audio.info.length

def get_m4b_length(file):
    if not file.endswith('.m4b'):
        return 0
    audio = MP4(file)
    return audio.info.length

def get_opus_length(file):
    if not file.endswith('.opus'):
        return 0
    tag = TinyTag.get(file)
    return tag.duration

def get_total_length(files):
    mp3sum = sum([get_mp3_length(file) for file in files])
    m4bsum = sum([get_m4b_length(file) for file in files])
    if use_opus:
        opussum = sum([get_opus_length(file) for file in files])
        return mp3sum + m4bsum + opussum
    else:
        return mp3sum + m4bsum

def seconds_to_hms(seconds):
    h = math.floor(seconds // 3600)
    m = math.floor(seconds % 3600 // 60)
    s = math.floor(seconds % 60)
    return '{:02}:{:02}:{:02}'.format(h, m, s)

def directory_report(path):
    dirs = get_directories(path)
    for dir in dirs:
        subdirs = get_directories(dir)
        if subdirs:
            directory_report(dir)
        files = get_media_files(dir)
        if len(files) == 0:
            continue
        audio_length = get_total_length(files)
        if audio_length == 0:
            continue
        if output_markdown:
            output.append({'dir': dir, 'length': audio_length})
            # print("|", end="")
            # print("|".join([f'{dir}', seconds_to_hms(audio_length)]), end="")
            # print("|")
        else:
            print(f'"{dir}"', end=', ')
            print(seconds_to_hms(audio_length))

sys.stdout.reconfigure(encoding='utf-8')
path = 'audiobooks'
if output_markdown:
    print("|Directory|Length|")
    print("|---|---|")
else:
    print('Directory, Length')
directory_report(path)
if output_markdown:
    output = sorted(output, key=lambda x: x['length'])
    for item in output:
        print(f'|{item["dir"]}|{seconds_to_hms(item["length"])}|')