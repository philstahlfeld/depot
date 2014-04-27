# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

from depot.automation.communication import message
from depot.automation.communication import action_message
from depot.automation.communication import board_messages
from depot.automation.communication import services_message
from depot.automation.communication import status_message


class BoardError(Exception):
  pass


class Board(object):

  def __init__(self, name):
    self.name = name
    self._services = {}
    self._hooks = []

  def AddService(self, service):
    if service.name in self._services:
      raise BoardError('Duplicate controller name: %s' % service.name)
    self._services[service.name] = service

  def AddHook(self, hook):
    self._hooks.append(name)

  def GetHooks(self):
    return self._hooks

  def __getitem__(self, key):
    return self._services[key]

  def Services(self):
    return self._services.values()


class BoardController(object):

  def __init__(self, board):
    self.board = board
    self.hook_handler = None  # Callable that takes hook and board as params.

  def HandleMessage(self, msg):
    if isinstance(msg, message.ServiceMessage):
      return self._HandleServiceMessage(msg)
    elif isinstance(msg, message.BoardMessage):
      return self._HandleBoardMessage(msg)
    else:
      print 'Cannot handle message'

  def _HandleServiceMessage(self, msg):
    service = self.board[msg.service_name]
    if isinstance(msg, status_message.StatusMessage):
      msg.status = service.Status()
      return msg
    elif isinstance(msg, action_message.ActionMessage):
      action = getattr(service.__class__, msg.action)
      if msg.args:
        print msg.args
      action(service, **msg.args)

  def _HandleBoardMessage(self, msg):
    if isinstance(msg, services_message.ServicesMessage):
      services = self.board.Services()
      for service in services:
        msg.AddService(service.name, service.flavor)
      return msg
    elif isinstance(msg, board_messages.HooksMessage):
      msg.hooks = self.board.GetHooks()
      return msg
    elif isinstance(msg, board_messages.HookTriggerMessage):
      self.hook_handler(hook=msg.hook, board=self.board)
