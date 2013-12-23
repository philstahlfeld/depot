import os
import subprocess
import sys
import time

requests_file = '/tmp/.requests'
interface = sys.argv[1]

os.system('urlsnarf -i %s libwaitress > %s' % (interface, requests_file))
