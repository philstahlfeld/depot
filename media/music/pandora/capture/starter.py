# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

import os
import subprocess
import sys
import time

requests_file = '/tmp/.requests'
interface = sys.argv[1]

os.system('urlsnarf -i %s libwaitress > %s' % (interface, requests_file))
