# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

import os

from depot.media.music.pandora.pianobar import config
from depot.media.music.pandora.pianobar import radio_info

def Start():
  if not radio_info.PianobarIsRunning():
    _RemoveInfo()
    os.system(config.STARTER_PATH)
    Play()

def Stop():
  os.system('pkill -9 -f pianobar')

def Play():
  _WriteToCtl('p')

def Next():
  _RemoveInfo()
  _WriteToCtl('n')

def VolumeUp():
  _WriteToCtl('))')

def VolumeDown():
  _WriteToCtl('((')

def ChangeStation(station_number):
  _RemoveInfo()
  _WriteToCtl('s')
  _WriteToCtl(station_number + '\n')


def _WriteToCtl(msg):
  with open(config.CTL_PATH, 'w') as ctl:
    ctl.write(msg)

def _RemoveInfo():
  os.system('rm %s' % config.INFO_PATH)
