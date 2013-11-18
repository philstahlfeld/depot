import pickle
import os
import re
import sys

CONFIG_DIR_PATH = os.path.expanduser('/home/philstahlfeld/.config/pianobar/')
CTL_PATH = CONFIG_DIR_PATH + 'ctl'
INFO_PATH = CONFIG_DIR_PATH + 'info'

def UpdateInfoFromEvent(event_action):
  """ Updates info file based on pianobar event and event info (from stdin) """

  if event_action == 'songstart':
    radio_info = RadioInfoFileStore()
    for line in sys.stdin:
      line = line.rstrip()
      if re.search('artist=', line):
        artist = line.split('=')[1]
        radio_info.artist = artist
      elif re.search('title=', line):
        song = line.split('=')[1]
        radio_info.song = song
      elif re.search('album=', line):
        album = line.split('=')[1]
        radio_info.album = album
      elif re.search('coverArt=', line):
        url = line.split('=')[1]
        radio_info.coverart_url = url
      elif re.search('stationName=', line):
        station = line.split('=')[1]
        radio_info.station = station
      elif re.search('station[0-9]+=', line):
        station = line.split('=')[1]
        radio_info.AddStation(station)

    radio_info.SaveToFile(INFO_PATH)


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
