"""Uses ffmpeg to convert audio files"""

import glob
import os
import re
import subprocess

from mutagen import easyid3

def MP4ToMP3(input_file, output_file=None, bitrate=192000):
  if not output_file:
    output_file = input_file[:-1] + '3'

  bitrate = str(bitrate)

  subprocess.call(['ffmpeg', '-i', input_file, '-f', 'mp3', '-ab', bitrate, '-vn', output_file])


def ConvertDir(directory):
  title_glob = '* BY * ON *'
  directory_glob = '%s/%s' % (directory, title_glob)
  files = glob.glob(directory_glob + '.mp4')
  for mp4 in files:
    MP4ToMP3(mp4)
    os.remove(mp4)

  files = glob.glob(directory_glob + '.mp3')
  for mp3 in files:
    print 'Working on ' + mp3
    pattern = re.compile('(.*/)(.+) (BY) (.+) (ON) (.+)(.mp3)')
    info = pattern.match(mp3)
    print info.groups()
    audio = easyid3.EasyID3(mp3)
    audio['title'] = info.group(2)
    audio['artist'] = info.group(4)
    audio['album'] = info.group(6)
    audio.save()
