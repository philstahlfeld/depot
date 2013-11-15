#!/usr/bin/python
import socket, ssl
import sys, traceback
import hashlib

from depot.raspberrypi.automation import message
from BoardController import BoardController
from OutletController import OutletController
from RGBController import RGBController

class Server(object):

    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    def setBoardController(self, bc):
        self.__boardController = bc

    def getBoardController(self):
        return self.__boardController

    def startServer(self):
        bindsocket = socket.socket()
        bindsocket.bind((self.__host, self.__port))
        bindsocket.listen(5)

        while True:
            newsocket, (ip, port) = bindsocket.accept()

            print "New connection from %s" % ip
            
            self.__conn = ssl.wrap_socket(newsocket,
                                    server_side = True,
                                    certfile = 'cert',
                                    keyfile = 'key',
                                    ssl_version = ssl.PROTOCOL_TLSv1)

            try:
                msg = message.recieveOverSocket(self.__conn)
                self.handleCurrentMessage(msg)
            except:
                print "An error occurred"
                traceback.print_exc(file=sys.stdout)
    
            self.__conn.close()

    def handleCurrentMessage(self, msg):
        """
            This method distributes the types of messages to be handled
        """
        h = "71f30df563d16be28f301c845e02bd4c501b3219b2fa4fe6f3a659e9a94f84e7"
        if hashlib.sha256(msg.getPassword()).hexdigest() != h:
            print "Authentication failed"
            return

        if isinstance(msg, message.BoardMessage):
            self.handleBoardMessage(msg)
        elif isinstance(msg, message.ControllerMessage):
            self.handleControllerMessage(msg)

    def handleControllerMessage(self, msg):

        if type(msg) is message.SwitchableMessage:
            print "Received SwitchableMessage"
            self.handleSwitchableMessage(msg)
            return

        if type(msg) is message.RGBMessage:
            print "Received RGBMessage"
            self.handleRGBMessage(msg)
            return

        print "Did not recognize message"


    def handleBoardMessage(self, msg):

        if type(msg) is message.BoardInformationMessage:
            print "Received BoardInformationMessage"
            self.handleBoardInformationMessage(msg)
            return

        print "Did not recognize message"


    def handleBoardInformationMessage(self, msg):
        bc = self.getBoardController()
        msg.SetName(bc.getName())
        
        cs = bc.getControllers()
        print "services %s" % len(cs)
        for c in cs:
            service = {}
            service["name"] = c.getName()
            service["type"] = c.getType()
            msg.AddService(service)

        msg.SendOverSocket(self.__conn)


        
    def handleSwitchableMessage(self, msg):
        """
            This message deals with all types of switchable messages
        """
        c = self.getBoardController().getControllerByName(msg.GetControllerName()) 
        if not c:
            return

        action = msg.GetAction()

        if action == message.SwitchableMessage.STATUS:
            print "    Status request on '{outlet}'".format(outlet = c.getName())
            status = c.getStatus()
            msg.AddOption('status', status)
            msg.SendOverSocket(self.__conn)

        elif action == message.SwitchableMessage.SWITCH_ON:
            c.turnOn()

        elif action == message.SwitchableMessage.SWITCH_OFF:
            c.turnOff()
        
        elif action == message.SwitchableMessage.TOGGLE:
            c.toggle()

    def handleRGBMessage(self, msg):
        c = self.getBoardController().getControllerByName(msg.GetControllerName()) 
        if not c:
            return

        action = msg.GetAction()

        if action == message.RGBMessage.STATUS:
            print "    Status request"

            status = c.getStatus()
            msg.SetRGB(status)
            msg.SendOverSocket(self.__conn)

        elif action == message.RGBMessage.SET_RGB:

            r,g,b = msg.GetRGB()
            print "    Setting RGB"
            c.adjustColor((r,g,b))

        


s = Server('', 14026)
bc = BoardController("The Birdhouse")
bc.addController(OutletController(12, "Outlet 3"))
bc.addController(OutletController(16, "Outlet 4"))
bc.addController(RGBController(red = 13, green = 15, blue = 11, name = "Fun Light"))

s.setBoardController(bc)
s.startServer()


