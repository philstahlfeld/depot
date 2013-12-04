from depot.automation.communication import message

class ServicesMessage(message.BoardMessage):

  def __init__(self):
    self.services = {}

  def AddService(self, name, flavor):
    self.services[name] = flavor
