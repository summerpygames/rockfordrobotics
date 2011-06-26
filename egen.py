# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 15:41:01 2011

@author: lucas
"""
from math import floor, sqrt
from random import choice

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

def egen(room, n, offset_x = 0, offset_y = 0, wave = False, rand = False, randnum = 0):
    if room[0] != room[1]:
        room = (room[0],room[0])
    if square(n):
        side = sqrt(n)
    else:
        after = n
        while square(after) == False:
            after += 1
        side = sqrt(after)
    #side refers to the number of enemies on the far right column
    size = room[0]/side
    return positions(room, n, size, side, offset_x, offset_y, wave, rand, randnum)

def positions(room, n, size, side, offset_x, offset_y, wave, rand, randnum):
    positions = []
    if rand:
        randinfo = []
        orignum = n
        n = randnum
        randlist = []
    elif wave is True:
        waveinfo = [(size,size)]
    if square(n):
        x = room[0]-size
        y = 0
        for i in range(int(n + sqrt(n))):
            if wave is True and even(i) is False:
                offset_y += size
            if y != room[0]:
                positions.append((int(x + offset_x),int(y + offset_y)))
                if rand:
                    randlist.append((int(x + offset_x),int(y + offset_y)))
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
        column = 1
        reset = 0
        for i in range(int(n + sqrt(n))):
            if reset == 1:
                offset_y -= size
                reset = 0
            if wave != 0 and even(column) is False:
                offset_y += size/2
                reset = 1
            if n == rem+before and multiple(n,side) == False:
                x = 0
                r = rem
                interval = (room[0]-r*size)/2
                y = interval
                for i in range(int(r/2)):
                    positions.append((int(x + offset_x),int(y + offset_y)))
                    if rand:
                        randlist.append((int(x + offset_x),int(y + offset_y)))
                    y += size + interval
                    rem -= 1
                y = room[0]-size/(side/2)-size
                for i in range(int(r/2)):
                    positions.append((int(x + offset_x),int(y + offset_y)))
                    if rand:
                        randlist.append((int(x + offset_x),int(y + offset_y)))
                    y -= size - interval
                    rem -= 1
                if rem == 1:
                    x = 0
                    y = floor((room[0]-size)/2)
                    positions.append((int(x + offset_x),int(y + offset_y)))
                    if rand:
                        randlist.append((int(x + offset_x),int(y + offset_y)))
                break
            if y < room[0]:
                positions.append((int(x + offset_x),int(y + offset_y)))
                if rand:
                    randlist.append((int(x + offset_x),int(y + offset_y)))
                rem -= 1
                y += size
            else:
                x -= size
                y = 0
                if wave is True:
                    column += 1
                    waveinfo.append(positions)
                    positions = []
    if wave is True:
        print waveinfo
        return waveinfo
    elif rand is True:
        print randlist
        for i in range(orignum):
            toappend = choice(randlist)
            randinfo.append(toappend)
            randlist.remove(toappend)
        print randinfo
        return ((size,size),randinfo)
    else:
        return ((size, size), positions)
egen((400,400),12, wave = True)
    