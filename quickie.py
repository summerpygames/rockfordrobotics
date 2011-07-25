#Import APH libraries
from APH import *
from APH.Game import *
from APH.Utils import *
from APH.Screen import *
from APH.Sprite import *

import pygame
import os
from olpcgames import svgsprite

class MovingSvgObject(Sprite):

    """Moving SVG Object extends SVGSprite to allow it to move.
    
    Use it the same way you would ues an SVGSprite
    
    """

    def __init__(self, position = (0, 0), svg=None, size=None, copy=False):

        if copy is not False and copy.__class__ == svgsprite.SVGSprite:
            self.sprite = copy.copy()
        else:
            data = open(svg).read()
            self.sprite = svgsprite.SVGSprite(data, size)

        super(MovingSvgObject, self).__init__()
        print self.sprite.image.get_flags()
        self.image = self.sprite.image
        self.rect = self.sprite.rect
        self.resolution = self.sprite.resolution
        self.rect.top = position[1]
        self.rect.left = position[0]
        self.change_x = 0
        self.change_y = 0
       
    def changespeed(self, x, y):
        """Change the speed of the SVG"""
        self.change_x+=x
        self.change_y+=y
        
    # Remap the new location of the SVG
    def update(self):
        """Update the location of the SVG"""
        self.rect.top += self.change_y
        self.rect.left += self.change_x
        super(MovingSvgObject, self).update()

#Image load function to avoid typing full path names
def my_load_image(imgName,colorkey=None):
    newName = os.path.join('data',imgName)
    return load_image(newName,colorkey)
        
class PlayState(SubGame):
    """The game state"""
    def __init__(self):
        SubGame.__init__(self)
        self.initialized = False        
    
    def transition_in(self):
        """Transition into the loop"""
        self.screen_state.set_background(my_load_image('deepspace.jpg'))

    def main_loop(self):
        GetScreen().draw()

class FancyNewState(SubGame):
    """The game state"""
    def __init__(self):
        SubGame.__init__(self)
        self.initialized = False        
    
    def transition_in(self):
        """Transition into the loop"""
        self.sprite = MovingSvgObject(position = (10, 10), svg = 'data/ufo.svg', size =(150, 150))
        self.group = Group(self.sprite)

    def main_loop(self):
        self.group.draw()
        GetScreen().draw()
#        pygame.display.update()
        


