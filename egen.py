# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 15:41:01 2011

@author: lucas
"""
from math import floor

def egen(size, i, offset = 0):
    position=[0,0]
    if size[1] <= 450:        
        if i == 0:
            position[0] = floor(size[0]-100+offset)
        elif i == 1:
            position[0] = floor(size[0]-100+offset)
            position[1] = floor(size[1]/2)
        elif i == 2:
            position[0] = floor(size[0]-200+offset)
            position[1] = floor(100)
        elif i == 3:
            position[0] = floor(size[0]-200+offset)
            position[1] = floor(size[1]/2+100)
    elif size[1] <= 650:
        if i == 0:
            position[0] = floor(size[0]-100+offset)
        elif i == 1:
            position[0] = floor(size[0]-100+offset)
            position[1] = floor(size[1]-100)
        elif i == 2:
            position[0] = floor(size[0]-200+offset)
            position[1] = floor(size[1]*3/4-100)
        elif i == 3:
            position[0] = floor(size[0]-200+offset)
            position[1] = floor(size[1]/2-size[1]/4-200)
    return (position[0],position[1])