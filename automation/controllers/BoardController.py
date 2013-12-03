from OutletController import OutletController

class BoardController(object):

    def __init__(self, name):
        self.__name = name
        self.__controllers = []

    def addController(self, controller):
        self.__controllers.append(controller)



    def getControllers(self):
        return self.__controllers

    def getControllerByName(self, name):
        for controller in self.getControllers():
            if name == controller.getName():
                return controller

        return None

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

