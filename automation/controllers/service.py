class Service(object):

  def __init__(self, name, flavor):
      self.name = name
      self.flavor = flavor

  def Status(self):
    raise NotImplementedError


class ServiceFlavor(object):

  def __init__(self, name):
    self.name = name
