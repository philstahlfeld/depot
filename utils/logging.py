import time

def Info(filename, message):
  _LogAtLevel(filename, message, 'INFO')

def Warn(filename, message):
  _LogAtLevel(filename, message, 'WARN')

def Error(filename, message):
  _LogAtLevel(filename, message, 'ERROR')

def _LogAtLevel(filename, message, level):
  with open(filename, 'a') as log:
    ts = time.asctime()
    output = '[%s] %s: %s' % (ts, level, message)
    print output
    log.write(output + '\n')

