import RPi.GPIO as GPIO
from multiprocessing import Pool
import atexit
import time

class RGBController(object):


    RED = 0
    GREEN = 1
    BLUE = 2

    def __init__(self, red, green, blue, name, freq = 500):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(red, GPIO.OUT)
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(blue, GPIO.OUT)

        self.__r = GPIO.PWM(red, freq)
        self.__g = GPIO.PWM(green, freq)
        self.__b = GPIO.PWM(blue, freq)
        
        self.__r.start(0)
        self.__g.start(0)
        self.__b.start(0)

        self.__r_dc = 0
        self.__g_dc = 0
        self.__b_dc = 0

        self.__name = name


    def getStatus(self):
        return (self.__r_dc, self.__g_dc, self.__b_dc)

    def adjustColor(self, (r, g, b), delay = 0):
        delay = delay / 3.0
        self.adjustComponent(RGBController.RED, int(r), delay)
        self.adjustComponent(RGBController.GREEN, int(g), delay)
        self.adjustComponent(RGBController.BLUE, int(b), delay)

    def adjustComponent(self, color, value, delay = 0):
        if color == RGBController.RED:
            color = self.__r
            old = self.__r_dc
            self.__r_dc = value
        elif color == RGBController.GREEN:
            color = self.__g
            old = self.__g_dc
            self.__g_dc = value
        elif color == RGBController.BLUE:
            color = self.__b
            old = self.__b_dc
            self.__b_dc = value
        else:
            print "Invalid color"
            return 

        if not 0 <= value <= 100:
            print "Invalid value"
            return
        elif value < old:
            trans = range(old, value - 1, -1)
        else:
            trans = range(old, value + 1, 1)

        delay = delay * 1.0 /len(trans)
        for dc in trans:
            color.ChangeDutyCycle(dc)
            time.sleep(delay)



    @atexit.register
    def __creanup():
        GPIO.cleanup()

    def getType(self):
        return "RGB"

    def getName(self):
        return self.__name
