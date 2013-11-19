import os

from depot.media.music.pandora.pianobar import config
from depot.media.music.pandora.pianobar import radio_info

def Start():
  if not radio_info.PianobarIsRunning():
    os.system(config.STARTER_PATH)

def Stop():
  os.system('pkill -9 -f pianobar')

def Play():
  _WriteToCtl('p')

def SwitchStation(station_number):
  _WriteToCtl('s')
  _WriteToCtl(station_number + '\n')


def _WriteToCtl(msg):
  with open(config.CTL_PATH, 'w') as ctl:
    ctl.write(msg)
