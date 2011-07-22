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
        self.render()
        
class Line(pygame.sprite.Sprite):

    """dA sprite that is a line"""

    def __init__(self, width)
        super(Line, self).__init__()
        self.line = pygame.Surface([width, 3])
        self.image = pygame.Surface([width, 3])
        self.image = pygame.Surface(size).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.line)
        self.rect = self.image.get_rect()


class FractionTerm(pygame.sprite.Sprite):

    """A numerator over a denomenator, no a mixed number, with a line"""

    def __init__(self, fint):
        super(FractionTerm, self).__init__()
        self.numerator = Letters(str(fint.num()))
        self.denomenator = Letters(str(fint.den()))
        if self.numerator.rect.width > self.denomenator.rect.width:
            self.width = self.numerator.rect.width()
        else:
            self.width = self.denomenator.rect.width()
        self.line = Line(self.width)

        MARGIN = 5

        self.dests = []
        srcs = [self.numerator, self.line, self.denomenator]

        cur_y = 0 # increments, how far from the top are we
        dw = self.width # The width of the destination sprite
        
        for src in srcs:
            self.dests.append((src, ((dw - src.get_width())/2), cur_y))
            cur_y += src.get_height() + MARGIN
        
        self.height = cur_y - MARGIN # sets the height to the fraction height
        
        self.image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        
        for src in dests:
            self.image.blit(src)

        



