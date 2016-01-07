import parLED.core.Interface
import parLED.core.Exceptions
import time


#def ValidateDevice(SerialRGB):
#    if (not isinstance(SerialRGB, parLED.core.Interface.SerialRGB)):
#        raise parLED.core.Exceptions.BadDevice
#    else:
#        return True



class InvalidDirection(Exception):
	def __init__(self, *args):
		message = "Invalid Direction"
		super(InvalidDirection, self).__init__(message, *args) 



def Blink(interval, repeat=False):
    """ This is a simple blink function.
        param:
            repeat 
                True = infinity
                int
    """
    pass
    
    if (not repeat):
        
def Slide(direction="right", reverse=False):
    if direction not in ["left", "right"]:
        raise InvalidDirection
    
    R = 255*3
    n = 0
    if (not reverse): r,g,b = (0,0,0)
    else:
        r,g,b = (255,255,255)
        #if (direction == "right"): r,g,b = (255,0,0)
        #elif (direction == "left"): r,g,b = (0,0,255)
        
    
    while (not n > R):
        if (direction == "left"):
            yield (b,g,r)
        elif (direction == "right"):
            yield (r,g,b)
        n += 1
        
        if (not reverse):
            if (r < 255) and (g is 0) and (b is 0):
                r += 1
            elif (r is 255):
                g += 1
                r -= 1
            elif (g > 0) and (r > 0):
                g += 1
                r -= 1            
            elif (g is 255):
                b += 1
                g -= 1
            elif (b > 0) and  (g > 0):
                b += 1
                g -= 1
        elif reverse:
            if (r is 255):
                r -= 1
            elif (g < 0) and (r < 0):
                g -= 1
                r -= 1
            elif (g is 0):
                g -= 1
            elif (g is 255):
                b += 1
                g -= 1
            elif (b > 0) and  (g > 0):
                b += 1
                g -= 1
        

s = parLED.core.Interface.SerialRGB("/dev/ttyUSB0")
while 1:
    try:
        #for c in Slide():
        #    s.change_color(c)
        #    time.sleep(0.001)

        for c in Slide():#direction="left"):
            s.change_color(c)
            time.sleep(0.001)
        time.sleep(4)
        s.change_color((255,0,0))
        time.sleep(.25)
        s.change_color((0,0,0))
        time.sleep(.25)
        s.change_color((255,0,0))
        time.sleep(4)
    except:
        break
