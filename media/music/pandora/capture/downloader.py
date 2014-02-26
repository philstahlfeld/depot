# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

import os
import urllib
import re

download_location = os.path.expanduser('~/Downloads/')
pattern = re.compile('(GET) (http://.*) (HTTP/)')

def DownloadLatest(title, artist, album):
  urls = []
  with open('/tmp/.requests', 'r') as f:
    for line in f:
      matches = pattern.search(line)
      if matches:
        urls.append(matches.group(2))
  
  latest = urls[-1]

  name = '%s BY %s ON %s' % (title, artist, album)
  urllib.urlretrieve(latest, download_location + name + '.mp4')
