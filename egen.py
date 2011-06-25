# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 15:41:01 2011

@author: lucas
"""
from math import floor, sqrt

def multiple(n, d):
    if n % d == 0:
        return True
    else:
        return False

def even(i):
    if i % 2 == 0:
        return True
    else:
        return False

def square(i):
    if sqrt(i) == floor(sqrt(i)):
        return True
    else:
        return False

def egen(room, n, offset_x = 0, offset_y = 0):
    if room[0] != room[1]:
        room = (room[0],room[0])
    if square(n):
        side = sqrt(n)
    else:
        after = n
        while square(after) == False:
            after += 1
        side = sqrt(after)
    size = room[0]/side
    return positions(room, n, size, side, offset_x, offset_y)

def positions(room, n, size, side, offset_x, offset_y):
    positions = []
    if square(n):
        x = room[0]-size
        y = 0
        for i in range(int(n + sqrt(n))):
            if y != room[0]:
                positions.append((int(x + offset_x),int(y + offset_y)))
                y += size
            else:
                x -= size
                y = 0
    else:
        before = n
        while multiple(before, side) == False:
            before -= 1
        x = room[0]-size
        y = 0
        rem = n
        for i in range(int(n + sqrt(n))):
            if n == rem+before and multiple(n,side) == False:
                x = 0
                r = rem
                if even(r+1) == False:
                    c = r + 2
                else:
                    c = r + 1
                odev = c - 1
                interval = (room[0]-odev*size)/c
                print interval
                y = 2 * interval
                for i in range(int(r/2)):
                    positions.append((int(x + offset_x),int(y + offset_y)))
                    y += size + interval
                    rem -= 1
                y = room[0]-size/(side/2)-size
                for i in range(int(r/2)):
                    positions.append((int(x + offset_x),int(y + offset_y)))
                    y -= size - interval
                    rem -= 1
                if rem == 1:
                    x = 0
                    y = floor((room[0]-size)/2)
                    positions.append((int(x + offset_x),int(y + offset_y)))
                break
            if y < room[0]:
                positions.append((int(x + offset_x),int(y + offset_y)))
                rem -= 1
                y += size
            else:
                x -= size
                y = 0
    print side
    print size
    print positions
    return ((size, size), positions)
egen((400, 400), 17)
