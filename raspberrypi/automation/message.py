import sys
import socket
import pickle

class Message(object):

  def __init__(self):
    self.__options = {}
    self.__auth = "x"

  def SetPassword(self, auth):
    self.__auth = auth

  def GetPassword(self):
    return self.__auth

  def AddOption(self, name, value):
    self.__options[name] = value

  def GetOption(self, name):
    if name in self.__options:
        return self.__options[name]
    return None 

  def SendOverSocket(self, s):
    # Send length of the Message
    serial = pickle.dumps(self)
    s.write(str(len(serial)).zfill(4))

    s.send(serial)

def RecieveOverSocket(s):
  msgLen = int(s.recv(4))

  buf = ""
  while len(buf) < msgLen:
      buf += s.read()

  return pickle.loads(buf)

class ControllerMessage(Message):
  """
      This is the base class for messages to send messages to actual pins
  """
  def __init__(self, boardName, controllerName):
    super(ControllerMessage, self).__init__()
    self.__boardName = boardName
    self.__controllerName = controllerName

  def GetBoardName(self):
    return self.__boardName

  def GetControllerName(self):
    return self.__controllerName

class SwitchableMessage(ControllerMessage):
  """
      This is class to send messages to anything that acts like a switch
  """

  STATUS = 0
  SWITCH_ON = 1
  SWITCH_OFF = 2
  TOGGLE = 3
  UPDATE_NAME = 4

  def __init__(self, boardName, controllerName, action):
    super(SwitchableMessage, self).__init__(boardName, controllerName)
    self.__action = action

  def GetAction(self):
    return self.__action

class RGBMessage(ControllerMessage):
  STATUS = 0
  SET_RGB = 1

  def __init__(self, boardName, controllerName, action):
    super(RGBMessage, self).__init__(boardName, controllerName)
    self.__action = action
    self.__rgb = None

  def SetRGB(self, (r,g,b)):
    self.__rgb = (r,g,b)

  def GetRGB(self):
    return self.__rgb

  def GetAction(self):
    return self.__action

class BoardMessage(Message):
	"""
		This is just a placeholder class
	"""
	pass


class BoardInformationMessage(BoardMessage):
	
	def __init__(self):
		super(BoardMessage,self).__init__()
		self.__name = ""
		self.__services = []

	def SetName(self, name):
		self.__name = name

	def GetName(self):
		return self.__name

	def AddService(self, service):
		self.__services.append(service)

	def GetServices(self):
		return self.__services
