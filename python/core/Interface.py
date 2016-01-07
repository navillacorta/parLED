#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial, time
from itertools import product

class SyncError(Exception):
    """Synchronisation error"""
    def __init__(self, msg=""):
        self._msg = str(msg)
    
    def __str__(self):
        return msg

class SerialRGB(object):
    wait = 0.00000001
    hold = 0.0
    
    def __init__(self, addr, baud=115200, **kwargs):
        """
        Creating a new SerialRGB object.
        
        addr -- The address of the serial port.
        baud -- The baudrate (default: 9600)
        """
        try:
            self.__ser = serial.Serial(addr, baud)
        except:
            raise IOError("Could not connect to Arduino via serial port.")
        # Sync...
        while self.__ser.inWaiting() < 1:
            self.__ser.write("\x00")
            time.sleep(.01)
        if self.__ser.read(1) != "1":
            raise SyncError
        
        self.__redVal = 0
        self.__grnVal = 0
        self.__bluVal = 0
        
        self.__prevR = self.__redVal
        self.__prevG = self.__grnVal
        self.__prevB = self.__bluVal
        
        #if (kwargs):
        #    if "debug" in kwargs.keys() and (kwargs["debug"]):
        #        self.tests = Tests(self)
        #        self.tests.basic_colors()
    
    def __del__(self):
        self.close_connection()
    
    @property
    def previousRGB(self):
        return (self.__prevR, self.__prevG, self.__prevB)
    
    @previousRGB.setter
    def previousRGB(self, (r,g,b)):
        self.__prevR, self.__prevG, self.__prevB = (r,g,b)
    
    @property
    def currentRGB(self):
        return (self.__redVal, self.__grnVal, self.__bluVal)
    
    @currentRGB.setter
    def currentRGB(self, (r,g,b)):
        self.__redVal, self.__grnVal, self.__bluVal = (r,g,b)
    
    def close_connection(self):
        """Closes the connection to the Arduino."""
        if self.__ser is not None:
            self.__ser.close()
            self.__ser = None
    
    def calculateStep(self, prevValue, endValue):
        step = endValue - prevValue
        if step:
            step = 1020/step
        return step
    
    def calculateVal(self, step, val, i):
        if (step) and  (i % step == 0):   # If step is non-zero and its time to change a value,
            if step > 0:
                val += 1                # increment the value if step is positive...
            elif step < 0:
                val -= 1                # ...or decrement it if step is negative
        
        #Defensive driving: make sure val stays in the range 0-255
        if val > 255:
            val = 255
        elif val < 0:
            val = 0
        return val
    
    def change_color(self, color):
        # store previous value
        self.previousRGB = self.currentRGB
        
        # store current value
        self.currentRGB = color
        self.__ser.write(self.currentRGB)
        if self.__ser.read(1) != "1":
            raise SyncError
        
    def cross_fade(self, color, wait=None, hold=None):
        if (not wait):
            wait = self.wait
        if (not hold):
            hold = self.hold
            
        # dont do anything if color is already set
        #if self.currentRGB == color:
        #    return
        R = color[0]
        G = color[1]
        B = color[2]
        
        stepR = self.calculateStep(self.__prevR, R)
        stepG = self.calculateStep(self.__prevG, G)
        stepB = self.calculateStep(self.__prevB, B)
        
        n = 0
        for n in range(1021):
            data = (
                self.calculateVal(stepR, self.__redVal, n),
                self.calculateVal(stepG, self.__grnVal, n),
                self.calculateVal(stepB, self.__bluVal, n)
                )
            
            self.change_color(data)
            # Pause for 'wait' milliseconds before resuming the loop
            time.sleep(wait)
            n += 1
            
        # Pause for optional 'wait' milliseconds before resuming the loop
        time.sleep(hold)
