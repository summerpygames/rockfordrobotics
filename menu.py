#!/usr/bin/env python
# menu.py
# Copyright (C) 2011 Mark Amber
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#Import APH libraries
from APH import *
from APH.Game import *
from APH.Utils import *
from APH.Screen import *
from APH.Sprite import *

import menuassets
from olpcgames import svgsprite
import olpcgames
import pygame
import logging


###########################################
##  For the Main Menu                    ##
###########################################

main = (
        (('play',  'D'),)
        (('how',  'UD'),)
        (('cred', 'UD'),)
        (('about', 'U'),)
       )

###########################################
##  For the Grades menu                  ##
###########################################

grades = (
          (('resume', 'D'), ('resume', 'D'  ), ('resume', 'D'))
          (('first', 'RU'), ('second', 'RLU'), ('third', 'LU'))
         )

###########################################
##  For the How to Play menu             ##
###########################################

# No buttons
how = ((('none', ''),),)

###########################################
##  For the Stage Selection Menu         ##
###########################################

stage = (
         (('deep',   'DR'), ('solar', 'DL'))
         (('planet', 'UR'), ('city',  'UL'))
        )

###########################################
##  For the About the Team Menu          ##
###########################################

# No buttons
how = ((('none', ''),),)

###########################################
##  For the Credits Menu                 ##
###########################################

# No buttons
how = ((('none', ''),),)

###Classes shared between states###
class Button(Sprite):
    """Base button class to be built upon"""
    def __init__(self, position = (0, 0), sel_svg=None, des_svg=None,
                 size=None, copy=False,
                 callout='NO', initsel=False):
        
        data_sel = open(sel_svg).read()
        data_des = open(des_svg).read()
        self.sprite_sel = svgsprite.SVGSprite(svg=data_sel, size=size)
        self.sprite_des = svgsprite.SVGSprite(svg=data_des, size=size)


        self.selected = initsel
        super(MovingSvgObject, self).__init__()
        if self.selected is True
            self.
        

        self.image = new_surface(self.sprite.image.get_size())
        self.image.blit(self.sprite.image, (0, 0))
        self.rect = self.sprite.rect
        self.resolution = self.sprite.resolution
        self.position = (position[0], position[1])
        self.position = position
        self.callout = callout
        
    def update(self, callout):
        """This will set the button to deselected if it was the thing
        that is now selected, and it will make itself selected if it is"""
        pass

###Classes for instructions###
class MainMenu(SubGame):
    """Class for the instruction pages"""
    def __init__(self):
        SubGame.__init__(self)
        self.initialized = False

    def transition_in(self):
        #General initialization
        if self.initialized:
            return
        self.cursor = [0, 0]
        self.initialized = True
        self.set_layers(['instructions'])
        self.t = 0        
        #Background initialization
        bg = my_load_image('instructionScreen.jpg')
        self.screen_state.set_background(bg)
        #Font & text initialization
        pygame.font.init()
        self.font = pygame.font.SysFont(None,80)
        #Sprite initialization

        self.backButton = baseButton('returnButton.png',(450,virtualHEIGHT-150))
        #Sprite group initialization
        self.group = Group()

    def main_loop(self):
        self.t = self.t + 1
        self.group.draw()
        GetScreen().draw()
        #Handle Button Clicks
        for event in Mouse.get_events():
            if self.backButton.detectCollision(event):
                self.pop_state()
        #Handle Other Events
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.pop_state()
            elif event.type == KEYDOWN and event.key == K_RETURN:
                self.pop_state()

