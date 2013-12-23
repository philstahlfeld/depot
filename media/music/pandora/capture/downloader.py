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
