#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       WhateverWeCallTheGame.py
#       
#       Copyright Contributors
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
# 
#Import APH libraries
from APH import *
from APH.Game import *
from APH.Utils import *
from APH.Screen import *
from APH.Sprite import *

import pygame
import olpcgames
from olpcgames import textsprite

class Letters(textsprite.TextSprite):

    """An element represenets a single piece of the probel.
    
    An element is either found in the answer or the question, such as 1 + 1 = 2
    in this situation 1 and 1 and 2 and + are elements, and they are all this
    type of element too, other elements can use multiple elements to make more
    impressive things
    
    """
    
    def __init__(self, string):
        super(Letters, self).__init__(text=str(string), size=32)
        self.render()
        
class Line(Sprite):

    """dA sprite that is a line"""

    def __init__(self, width):
        super(Line, self).__init__()
        self.image = pygame.Surface([width, 3])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()


class FractionTerm(Sprite):

    """A numerator over a denomenator, no a mixed number, with a line"""

    def __init__(self, fint):
        super(FractionTerm, self).__init__()
        self.numerator = Letters(str(fint.num()))
        self.denomenator = Letters(str(fint.den()))
        if self.numerator.rect.width > self.denomenator.rect.width:
            self.width = self.numerator.rect.width
        else:
            self.width = self.denomenator.rect.width
        self.line = Line(self.width)

        MARGIN = 5

        self.dests = []
        srcs = [self.numerator, self.line, self.denomenator]

        cur_y = 0 # increments, how far from the top are we
        dw = self.width # The width of the destination sprite
        
        for src in srcs:
            self.dests.append( (src.image,
                                (((dw - src.rect.width)/2), cur_y)
                               ))
            cur_y += src.rect.height + MARGIN
        
        self.height = cur_y - MARGIN # sets the height to the fraction height
        
        self.image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        
        for src in self.dests:
            self.image.blit(*src)

        



