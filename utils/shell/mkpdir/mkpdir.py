#!/usr/bin/python

import sys
import os

path = sys.argv[1]

os.system('mkdir %s' % path)
os.system('echo "" > %s/__init__.py' % path)
