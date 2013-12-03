import RPi.GPIO as GPIO
import atexit

class OutletController(object):
    
    __counter = 0

    def __init__(self, pinNumber, name = None):
        self.__pinNumber = pinNumber
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pinNumber, GPIO.OUT)
        GPIO.output(self.__pinNumber, GPIO.LOW)

        if name:
            self.__name = name
        else:
            self.__name = "outlet%s" % OutletController.__counter

        OutletController.__counter += 1

    def toggle(self):
        GPIO.output(self.__pinNumber, not GPIO.input(self.__pinNumber))

    def getStatus(self):
        return GPIO.input(self.__pinNumber)

    def turnOn(self):
        GPIO.output(self.__pinNumber, GPIO.HIGH)

    def turnOff(self):
        GPIO.output(self.__pinNumber, GPIO.LOW)

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getType(self):
        return "SWITCHABLE"
		
    @atexit.register
    def __cleanup():
        """ Automatically returns pins to inputs at end of usage """
        GPIO.cleanup()

	
