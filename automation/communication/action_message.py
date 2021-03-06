# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <phil@stahlfeld.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Phil Stahlfeld
# ----------------------------------------------------------------------------

from depot.automation.communication import message


class ActionMessage(message.ServiceMessage):

  def __init__(self, service_name, action, **kwargs):
    super(ActionMessage, self).__init__(service_name)
    self.action = action.__name__
    self.args = kwargs
