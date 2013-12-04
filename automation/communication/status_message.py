from depot.automation.communication import message

class StatusMessage(message.ServiceMessage):

  def __init__(self, service_name):
    super(StatusMessage, self).__init__(service_name)
    self.status = None
