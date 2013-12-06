from depot.automation.communication import message

class ActionMessage(message.ServiceMessage):

  def __init__(self, service_name, action, **kwargs):
    super(ActionMessage, self).__init__(service_name)
    self.action = action.__name__
    self.args = kwargs
