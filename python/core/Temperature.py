#!/usr/bin/env python

# if im freezing, im probably not gonna be interested in what range i put here
FARENHEIT_MIN = 14
FARENHEIT_MAX = 122

CELSIUS_MIN = -10
CELSIUS_MAX = 50

def temp2rgb(minval, maxval, val, colors=[(0, 0, 255), (0, 255, 0), (255, 0, 0)]):
    # stay within rgb range (0,0,0) - (255,255,255)
    if val <= minval:
        val = minval
    max_index = len(colors)-1
    v = float(val-minval) / float(maxval-minval) * max_index
    i1, i2 = int(v), min(int(v)+1, max_index)
    (r1, g1, b1), (r2, g2, b2) = colors[i1], colors[i2]
    f = v - i1
    return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

    
def farenheit2rgb(deg):
    return temp2rgb(FARENHEIT_MIN, FARENHEIT_MAX, deg)

    
def celsius2rgb(deg):
    return temp2rgb(CELSIUS_MIN, CELSIUS_MAX, deg)
