#!/usr/bin/python
import pygame
#from olpcgames import pangofont
import re
import sprites

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

        
        # Set what operation we are using
        self.operation  = question['operation']
        # Set the attributes for this instance to what we recieved from the db
        self.term1 = self.extractor(str(question['term1']))
        self.term2 = self.extractor(str(question['term2']))
        self.right = self.extractor(str(question['right']))
        self.wrong1 = self.extractor(str(question['wrong1']))
        self.wrong2 = self.extractor(str(question['wrong2']))
        self.wrong3 = self.extractor(str(question['wrong3']))
        
        

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
                
    def __decide(self):
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
            if (isinstance(self.term1, fint) or isinstance(self.term2, fint)):
                # If either number is a fraction
                return 'Fract'
            else:
                if (self.term1 > 10 or self.term2 > 10):
                    return 'Vertical'
                else:
                    return 'Flat'

        elif self.operation == '-':
            if (isinstance(self.term1, fint) or isinstance(self.term2, fint)):
                # If either number is a fraction
                return 'Fract'
            else:
                if (self.term1 > 10 or self.term2 > 10):
                    return 'Vertical'
                else:
                    return 'Flat'

        elif self.operation == '*':
            if (isinstance(self.term1, fint) or isinstance(self.term2, fint)):
                # If either number is a fraction
                return 'Fract'
            else:
                if (self.term1 > 10 or self.term2 > 10):
                    return 'Vertical'
                else:
                    return 'Flat'

        elif self.operation == '/':
            if (isinstance(self.term1, fint) or isinstance(self.term2, fint)):
                # If either number is a fraction
                return 'Fract'
            else:
                if (self.term1 > 10 or self.term2 > 10):
                    return 'Div'
                else:
                    return 'Flat'

        else:

class Question(pygame.sprite.Sprite):

    """This will make a surface using fonts from the olpc from a question
    
    it will look at the problem, find out what it should look like, then print
    out a visual represenation of the whole thing on the surface

    """

    def __init__(self, arg):
        pass
        

class Answer(pygame.sprite.Sprite):

    """docstring for DrawIt"""
    
    def __init__(self, ):
        pass        

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

    def __int__(self):
        return self.__i

    def __gt__(self, value):
        return (self.__i > value)

    def __lt__(self, value):ClassName
        return (self.__i < value)

def create_rint(i_in, r_in):
    """Factory to construct, and return, the proper object
    
    This will return an intager if the remainder happens to be 0 and return a
    rint if it has a non-zero remainder
    """
    i = int(i_in)
    r = int(r_in)
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

    def __int__(self):
        return self.__num

    def __gt__(self, value):
        return (self.__num > value)

    def __lt__(self, value):
        return (self.__num < value)
        
class fmint(fint):

    """A fraction with a whole number and a fraction"""
    
    def __init__(self, whole, num, den):
        super(fmint, self).__init__(num, den)
        self.__whole = whole

    def whole(self):
        """Return the whole number"""
        return self.__whole

def create_fint(whole_in, num_in, den_in):
    """Factory to construct and return the proper object
    this will return an intager if there is no fraction, a fraction if there is
    no whole number, and a mixed number if all spots are non-zero
    """
    whole = int(whole_in)
    num = int(num_in)
    den = int(den_in)
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
