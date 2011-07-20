#!/usr/bin/python
import pygame
from olpcgames import pangofont
import re

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
        self.operations  = (create_rint,
                            create_fint,
                            int)
        
        # Set what operation we are using
        self.operation  = question['operation']
        # Set the attributes for this instance to what we recieved from the db
        self.term1      = self.extractor(question['term1'])
        self.term2      = self.extractor(question['term2'])
        self.right      = self.extractor(question['right'])
        self.wrong1     = self.extractor(question['wrong1'])
        self.wrong2     = self.extractor(question['wrong2'])
        self.wrong3     = self.extractor(question['wrong3'])
        
        

    def extractor(self, string):
        """Find what kind of number we have using regex"""
        for r, x in zip(self.expressions, self.operations):
            self.m = r.match(string) # Create a match object
            
            try:
                self.g = m.groups()
            except AttributeError:
                pass
            else:
                return x(*self.g)
            
                
        

class Draw(object):

    """This will make a surface using fonts from the olpc from a question
    
    it will look at the problem, find out what it should look like, then print
    out a visual represenation of the whole thing on the surface

    """

    def __init__(self, arg):
        self.arg = arg
        

class DrawTheAnswer(Draw):
    """docstring for DrawIt"""
    def __init__(self, ):
        self.arg = arg
        
class DrawTheQuestion(Draw):

    """docstring for DrawTheQuestion"""

    def __init__(self, term_1, term_2, operation, result):
        self. = arg
        
class rint(object):

    """An intager with a remainder, for answering questions"""

    def __init__(self, i, r):
        self.__i = i
        self.__r = r

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

def create_rint(i, r):
    """Factory to construct, and return, the proper object
    
    This will return an intager if the remainder happens to be 0 and return a
    rint if it has a non-zero remainder
    """
    if r == 0:
        return i

    else:
        return rint(i, r)

class fint(object):

    """A set of two intagers, one numerator one denomenator"""

    def __init__(self, num, den):
        self.__num = num
        self.__sen = den

    def num(self):
        """Return the Numerator"""
        return self.__num

    def den(self):
        """Retrun the Denomenator"""
        return self.__den
        
class fmint(fint):

    """A fraction with a whole number and a fraction"""
    
    def __init__(self, whole, num, den):
        super(fint, self).__init__(num, den)
        self.__whole = whole

    def whole(self):
        """Return the whole number"""
        return self.__whole

def create_fint(whole, num, den):
    """Factory to construct and return the proper object
    this will return an intager if there is no fraction, a fraction if there is
    no whole number, and a mixed number if all spots are non-zero
    """
    if abs(whole) == 0:# make sure it has no whole number
        if num != den: # make sure it is not a whole number like 1/1
            return fint(num, den)
        else: # in the case that the num and den are the same
            return int(num)
    elif num == 0: # in the case that there is no fraction part
        return whole
    else: # in the case that we have all three elements
        return fmint(whole, num, den)
        

if __name__ == '__main__':
    main()
