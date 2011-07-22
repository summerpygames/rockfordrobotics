import pygame
import olpcgame
from olpcgame import textsprite

class Letters(textsprite.TextSprite):

    """An element represenets a single piece of the probel.
    
    An element is either found in the answer or the question, such as 1 + 1 = 2
    in this situation 1 and 1 and 2 and + are elements, and they are all this
    type of element too, other elements can use multiple elements to make more
    impressive things
    
    """
    
    def __init__(self, string):
        super(Element, self).__init__(text=string, size=32)
        
        

    def width(self):
        """
        Returns the width of this
        """
        
class Line(pygame.sprite.Sprite):
    """docstring for Line"""
    def __init__(self, width)
        super(Line, self).__init__()
        self.line = pygame.Surface([width, 3])
        self.image = pygame.Surface([width, 3])
        self.image.blit(self.line)

class FractionTerm(pygame.sprite.Sprite):
    """A numerator over a denomenator, no a mixed number, with a line"""
    def __init__(self, fint):
        super(FractionTerm, self).__init__()
        self.numerator = Letters(str(fint.num()))
        self.denomenator = Letters(str(fint.den()))
        self.line = Line
        
        

        



