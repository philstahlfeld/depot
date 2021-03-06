# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

import socket
import threading
import time

from depot.automation.communication import action_message
from depot.automation.communication import board_messages
from depot.automation.communication import message
from depot.automation.communication import services_message
from depot.automation.communication import status_message


class RemoteManager(object):

  def __init__(self, name, remote_ip, remote_port):
    self._ip = remote_ip
    self._port = remote_port
    self.services = {}  # Map service name to (flavor, status)
    self._update = True  # Keep thread going
    self._name = name
    self._services_lock = threading.Lock()
    self.hooks = []  # Hooks that this board has

  def _OpenSocket(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((self._ip, self._port))
    return s

  def Start(self):
    self._update = True
    t = threading.Thread(target=self._RunUpdater)
    t.daemon = True
    t.start()

  def Stop(self):
    self._update = False

  def PerformAction(self, service_name, action, **kwargs):
    msg = action_message.ActionMessage(service_name=service_name,
                                       action=action,
                                       **kwargs)
    s = self._OpenSocket()
    msg.SendOverSocket(s)
    s.close()
    self._Update()

  def TriggerHook(self, hook):
    if hook in self.hooks:
      s = self._OpenSocket()
      msg = board_messages.HookTriggerMessage(hook)
      msg.SendOverSocket(s)
      s.close()

  def _RunUpdater(self):
    while self._update:
      self._Update()
      time.sleep(5)

  def _Update(self):
    # Get services
    s = self._OpenSocket()
    msg = services_message.ServicesMessage()
    msg.SendOverSocket(s)
    msg = message.ReceiveOverSocket(s)
    s.close()
    services = {}
    for name in msg.services:
      s = self._OpenSocket()
      msg2 = status_message.StatusMessage(name)
      msg2.SendOverSocket(s)
      msg2 = message.ReceiveOverSocket(s)
      s.close()
      services[name] = (msg.services[name], msg2.status)

    # Get hooks
    s = self._OpenSocket()
    msg = board_messages.HooksMessage()
    msg.SendOverSocket(s)
    msg = message.ReceiveOverSocket(s)
    s.close()
    hooks = msg.hooks

    with self._services_lock:
      self.services = services
      self.hooks = hooks

  def __repr__(self):
    rtn = '%s\n' % self._name
    for name in self.services:
      flavor = self.services[name][0].name
      status = self.services[name][1]
      rtn += '  %s => (%s, %s)\n' % (name, flavor, status)
    return rtn

if __name__ == '__main__':
  mgr = RemoteManager('Birdhouse', '10.1.10.17', 14025)
  mgr.Start()
  print mgr
