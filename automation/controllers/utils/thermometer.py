# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

import os
import glob
import time


base_dir = '/sys/bus/w1/devices/'

def _ReadTempRaw():
  device_folder = glob.glob(base_dir + '28*')[0]
  device_file = device_folder + '/w1_slave'
  f = open(device_file, 'r')
  lines = f.readlines()
  f.close()
  return lines

def _ReadTemp():
  lines = _ReadTempRaw()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = _ReadTempRaw()
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c, temp_f

def GetTemperature(celsius=False):
  os.system('modprobe w1-gpio')
  os.system('modprobe w1-therm')

  if not celsius:
    return _ReadTemp()[1]
  else:
    return _ReadTemp()[0]

