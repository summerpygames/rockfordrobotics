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

def answergen(offset_x, offset_y, screensize):
    """Generate the posisions for answer guys"""
    PADDING = screensize[1]/32
    SIZE = (
            (screensize[1] - (3*PADDING)) / 4,
            (screensize[1] - (3*PADDING)) / 4
           )
    pos = []
    x = 0
    y = 0
    for i in range(3):
        pos.append((int(x + offset_x),int(y + offset_y)))
        y += PADDING + SIZE[1]
    pos.append((int(x + offset_x),int(y + offset_y)))

    return (SIZE, pos)


def positions(room, n, size, side, offset_x, offset_y, wave, rand, randnum):
    positions = []
    reset = 0
    column = 1
    if rand:
        randinfo = []
        orignum = n
        n = randnum
        randlist = []
    elif wave is True:
        wavepos = []
        offset_y_orig = offset_y
    if square(n):
        x = room[0]-size
        y = 0
        for i in range(int(n + sqrt(n))):
            if reset:
                offset_y = offset_y_orig - size/2
            if wave is True and even(column) is False:
                offset_y = offset_y_orig + size/2
                reset = True
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
        for i in range(int(n + sqrt(n))):
            if reset == 1:
                offset_y = offset_y_orig - size/2
                reset = 0
            if wave is True and even(column) is False:
                offset_y = offset_y_orig + size/2
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
            elif y < room[0]:
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
                    wavepos.append(positions)
                    positions = []
    if wave is True:
        return ((size,size),wavepos)
    elif rand is True:
        for i in range(orignum):
            toappend = choice(randlist)
            randinfo.append(toappend)
            randlist.remove(toappend)
        return ((size,size),randinfo)
    else:
        return ((size, size), positions)
