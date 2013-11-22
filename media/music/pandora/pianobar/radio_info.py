import pickle
import os
import re
import sys

from depot.media.music.pandora.pianobar import config


def GetCurrentRadioInfo():
  try:
    return RadioInfoFileStore.LoadFromFile(config.INFO_PATH)
  except:
    return None

def UpdateInfoFromEvent(event_action):
  """ Updates info file based on pianobar event and event info (from stdin) """

  if event_action == 'songstart':
    radio_info = RadioInfoFileStore()
    for line in sys.stdin:
      line = line.rstrip()
      if re.search('artist=', line):
        artist = line.split('=')[1]
        radio_info.artist = artist.strip()
      elif re.search('title=', line):
        song = line.split('=')[1]
        radio_info.song = song.strip()
      elif re.search('album=', line):
        album = line.split('=')[1]
        radio_info.album = album.strip()
      elif re.search('coverArt=', line):
        url = line.split('=')[1]
        radio_info.coverart_url = url.strip()
      elif re.search('stationName=', line):
        station = line.split('=')[1]
        radio_info.station = station.strip()
      elif re.search('station[0-9]+=', line):
        station = line.split('=')[1].strip()
        radio_info.AddStation(station)

    radio_info.SaveToFile(config.INFO_PATH)


class RadioInfoFileStore(object):

  def __init__(self):
    self.song = None
    self.artist = None
    self.album = None
    self.coverart_url = None
    self.station = None
    self.stations = []

  def AddStation(self, station_name):
    self.stations.append(station_name)

  def SaveToFile(self, file_name):
    with open(file_name, 'w') as store:
      pickle.dump(self, store)

  @staticmethod
  def LoadFromFile(file_name):
    with open(file_name, 'r') as store:
      return pickle.load(store)

  def __eq__(self, other):
    return (self.song == other.song and 
            self.artist == other.artist and
            self.album == other.album and 
            self.coverart_url == other.coverart_url and
            self.station == other.station)

  def __ne__(self, other):
    return not self.__eq__(other)

def PianobarIsRunning():
  l = os.popen('ps -ef | grep pianobar').read().split('\n')
  return len(l) > 3
