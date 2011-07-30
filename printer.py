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
import assets
#from olpcgames import pangofont
import re
import sprites

class Rint(object):

    """An intager with a remainder, for answering questions """

    def __init__(self, i, r):
        self.__i = i
        self.__r = r
        self.type = 'rint'

    def i(self):
        """Return the int part"""
        return self.__i

    def r(self):
        """Return the remainder part"""
        return self.__r

    def isrzero(self):
        """Test if the reaminder is 0"""
        if self.__r is 0:
            return True
        else:
            return False

    def __int__(self):
        return self.__i

    def __gt__(self, value):
        return (self.__i > value)

    def __lt__(self, value):
        return (self.__i < value)

def create_Rint(i_in, r_in):
    """Factory to construct, and return, the proper object
    
    This will return an intager if the remainder happens to be 0 and return a
    rint if it has a non-zero remainder
    """
    i = int(i_in)
    r = int(r_in)
    if r == 0:
        return i

    else:
        return Rint(i, r)

class Fint(object):

    """A set of two intagers, one numerator one denomenator"""

    def __init__(self, num, den):
        self.__num = num
        self.__den = den
        self.type = 'fint'
        self.isfraction = True

    def num(self):
        """Return the Numerator"""
        return self.__num

    def den(self):
        """Retrun the Denomenator"""
        return self.__den

    def __int__(self):
        return self.__num

    def __gt__(self, value):
        return (self.__num > value)

    def __lt__(self, value):
        return (self.__num < value)

    def __repr__(self):
        return '{0}/{0}'.format(self.__num, self.__den)

        
class FMint(Fint):

    """A fraction with a whole number and a fraction"""
    
    def __init__(self, whole, num, den):
        super(FMint, self).__init__(num, den)
        self.__whole = whole
        self.type = 'fmint'

    def whole(self):
        """Return the whole number"""
        return self.__whole

    def __repr__(self):
        return '{0}/{1}/{2}'.format(self.__whole, self.__num, self.__den)

def create_Fint(whole_in, num_in, den_in):
    """Factory to construct and return the proper object
    this will return an intager if there is no fraction, a fraction if there is
    no whole number, and a mixed number if all spots are non-zero
    """
    whole = int(whole_in)
    num = int(num_in)
    den = int(den_in)
    if abs(whole) == 0:# make sure it has no whole number
        if num != den: # make sure it is not a whole number like 1/1
            return Fint(num, den)
        else: # in the case that the num and den are the same
            return int(num)
    elif num == 0: # in the case that there is no fraction part
        return whole
    else: # in the case that we have all three elements
        return FMint(whole, num, den)

def decideelement(element):
        """Use this to return what sprite drawer should be used
        
        This will return a Letters element for an int, a FractionElelment for...
        """

        if isinstance(element, int):
            return sprites.Letters(element)
        else:
            try:
                if element.type == 'fint':
                    r = sprites.FractionTerm
                elif element.type == 'fmint':
                    r = sprites.FractionTerm
                elif element.type == 'rint':
                    r = sprites.RemainderTerm
                else:
                    r = sprites.Letters
            except AttributeError:
                r = sprites.Letters
            finally:
                return r(element)


class Question(Sprite):

    """This will make a surface using fonts from the olpc from a question
    
    it will look at the problem, find out what it should look like, then print
    out a visual represenation of the whole thing on the surface

    """

    def __init__(self):
        super(Question, self).__init__()
    
    def create(self, width, height):
        """Create the image"""
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()


    

class FlatQuestion(Question):
    """A question in the right to left format"""
    def __init__(self, term1, operation, term2):
        super(FlatQuestion, self).__init__()
        self.term1 = term1
        self.term2 = term2
        self.operation = operation
        self.term1_sprite = decideelement(self.term1)
        self.term2_sprite = decideelement(self.term2)
        self.operation_sprite = decideelement(self.operation)

        self.height = max((self.term1_sprite.rect.height,
                           self.term2_sprite.rect.height,
                           self.operation_sprite.rect.height))

        self.line = sprites.Line(100)
        self.equals = sprites.Letters("=")

        MARGIN = 5 # The margin between parts of the question

        self.dests = []
        srcs = [self.term1_sprite, self.operation_sprite, self.term2_sprite,
                self.equals]

        cur_x = 0 # increments, how far from the left are we
        dh = self.height # The width of the destination sprite
        
        for src in srcs:
            self.dests.append( (src.image,

                                (cur_x, ( (dh - src.rect.height) / 2 ))

                               ))
            cur_x += src.rect.width + MARGIN

        self.dests.append((self.line.image,
                           (cur_x, (dh - self.line.rect.height))
                          ))
        cur_x += self.line.rect.width
        self.width = cur_x# sets the height to the fraction height

        super(FlatQuestion, self).create(self.width, self.height)


                
        for src in self.dests:
            self.image.blit(*src)


class VerticalQuestion(Question):
    """A question in the right to left format"""
    def __init__(self, term1, operation, term2):
        super(VerticalQuestion, self).__init__()
        self.term1 = term1
        self.term2 = term2
        self.operation = operation
        self.term1_sprite = decideelement(self.term1)
        self.term2_sprite = decideelement(self.term2)
        self.operation_sprite = decideelement(self.operation)
        
        self.width  = max((self.term1_sprite.rect.width,
                           self.term2_sprite.rect.width,
                           self.operation_sprite.rect.width,
                           100))

        

        MARGIN = 5 # The margin between parts of the question

        self.dests = []
        srcs = [self.term1_sprite, self.operation_sprite, self.term2_sprite,]

        cur_y = 0 # increments, how far from the left are we
        dh = self.width # The width of the destination sprite
        
        for src in srcs:
            self.dests.append( (src.image,
                                ((dh - src.rect.height), cur_y)
                               ))
            cur_y += src.rect.height + MARGIN
        
        self.line = sprites.Line(self.width)

        self.dests.append((self.line.image,
                           (cur_y, (dh - self.line.rect.height))
                          ))
        cur_y += self.line.rect.height
        self.height = cur_y# sets the height to the fraction height

        super(VerticalQuestion, self).create(self.width, self.height)


                
        for src in self.dests:
            self.image.blit(*src)



class Answer(Sprite):

    """docstring for DrawIt"""
    
    def __init__(self, ):
        pass        

class FlatAnswer(Answer):
    """Make a """
    def __init__(self, arg):
        super(FlatAnswer, self).__init__()
        self.arg = arg

class Converter(object):
    
    """Full solution to turn an entry from a database into a bunch of surfaces

    Provide this with the dict from the database and let it work its magic, also
    provide the type of operation being performed, that way it will be east to
    know what it should print on the screen
    
    """
    
    def __init__(self, question):

        # Setup the ways to test the string, the order is important
        self.expressions = (re.compile(r"(\d+)R(\d+)"),
                            re.compile(r"(\d+)/(\d+)/(\d+)"),
                            re.compile(r"(\d+)"))
        self.operations  = (create_Rint,
                            create_Fint,
                            int)

        
        # Set what operation we are using
        self.operation  = question['operation']
        # Set the attributes for this instance to what we recieved from the db
        self.term1 = self.extractor(str(question['term1']))
        self.term2 = self.extractor(str(question['term2']))
        self.right = self.extractor(str(question['right']))
        self.wrong1 = self.extractor(str(question['wrong1']))
        self.wrong2 = self.extractor(str(question['wrong2']))
        self.wrong3 = self.extractor(str(question['wrong3']))

        self.kind = self.decidequestion()

    def render(self):
        """Render the right and wrong answers and put them in a list of tuples"""
        self.responses = []
        self.responses.append((decideelement(self.right), True))
        for i in [self.wrong1, self.wrong2, self.wrong3]:
            self.responses.append((decideelement(i), False))
        
    def getquestion(self):
        """Return the question for putting on the screen"""
        return self.kind(self.term1, self.operation, self.term2)

    def extractor(self, string):
        """Find what kind of number we have using regex"""
        for r, x in zip(self.expressions, self.operations):
            self.m = r.match(string) # Create a match object
                        
            try:
                self.g = self.m.groups()
            except AttributeError:
                pass
            else:
                return x(*self.g)

                
    def decidequestion(self):
        """ Method to decide what format we will be displaying the problem in
        
        To make it easy to understand, the code is heavily commented so you can
        follow the structure of how you figgure out what kind of display to use
        but in general, you could end up with:
        Flat + Flat = ____
        
         -or-
         
         Vertical
        +Vertical
        _________
        
         -or-
         
        Fract    Fract   Fract
        ----  +  ----- = -----
        Fract    Fract   Fract
        
         -or-
           ______         
        Div) Div
 
        and the return is the class that will build this type of equation.
        
        """
        
        if self.operation == '+':
            try:
                if (self.term1.isfraction or self.term2.isfraction):
                    # If either number is a fraction
                    return FlatQuestion
            except AttributeError:
                if (self.term1 > 10 or self.term2 > 10):
                    return VerticalQuestion
                else:
                    return FlatQuestion

        elif self.operation == '-':
            try:
                if (self.term1.isfraction or self.term2.isfraction):
                    # If either number is a fraction
                    return FlatQuestion
            except AttributeError:
                if (self.term1 > 10 or self.term2 > 10):
                    return VerticalQuestion
                else:
                    return FlatQuestion

        elif self.operation == '*':
            try:
                if (self.term1.isfraction or self.term2.isfraction):
                    # If either number is a fraction
                    return FlatQuestion
            except AttributeError:
                if (self.term1 > 10 or self.term2 > 10):
                    return VerticalQuestion
                else:
                    return FlatQuestion

        elif self.operation == '/':
            try:
                if (self.term1.isfraction or self.term2.isfraction):
                    # If either number is a fraction
                    return FlatQuestion
            except AttributeError:
                if (self.term1 > 10 or self.term2 > 10):
                    return FlatQuestion
                else:
                    return FlatQuestion

        else:
            pass

        

if __name__ == '__main__':
    main()
