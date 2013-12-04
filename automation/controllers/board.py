from depot.automation.communication import message
from depot.automation.communication import action_message
from depot.automation.communication import services_message
from depot.automation.communication import status_message

class BoardError(Exception):
  pass

class Board(object):

  def __init__(self, name):
    self.name = name
    self._services = {}

  def AddService(self, service):
    if service.name in self._services:
      raise BoardError('Duplicate controller name: %s' % service.name)
    self._services[service.name] = service

  def __getitem__(self, key):
    return self._services[key]

  def Services(self):
    return self._services.values()


class BoardController(object):

  def __init__(self, board):
    self.board = board

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
      msg.action(service, **msg.args)

  def _HandleBoardMessage(self, msg):
    if isinstance(msg, services_message.ServicesMessage):
      services = self.board.Services()
      for service in services:
        msg.AddService(service.name, service.flavor)
        return msg
