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

from assets import *
from olpcgames import svgsprite, textsprite
import olpcgames
import pygame
import logging
import os


###########################################
##  For the Main Menu                    ##
###########################################

mainmen = (
           (('play',  'D'),),
           (('how',  'UD'),),
           (('cred', 'UD'),),
           (('about', 'U'),)
          )

###########################################
##  For the Grades menu                  ##
###########################################

grades = (
          (('resume', 'D'), ('resume', 'D'  ), ('resume', 'D')),
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
         (('deep',   'DR'), ('solar', 'DL')),
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
    def __init__(self, position = (0, 0), #starting position?
                 sel_svg=None, des_svg=None, # images
                 size=None, # only spec the vertical/hor size
                 callout='NO', # Name to respond to select
                 initsel=False, # Select this on start
                 trigger=None):  # what should be done on a trigger
        
        data_sel = open(sel_svg).read()
        data_des = open(des_svg).read()
        self.sprite_sel = svgsprite.SVGSprite(svg=data_sel, size=size)
        self.sprite_des = svgsprite.SVGSprite(svg=data_des, size=size)
        print self.sprite_sel.image.get_size()

        self.selected = initsel
        Sprite.__init__(self)
        self.image = new_surface(self.sprite_sel.image.get_size())
        if self.selected is True:
            self.image.blit(self.sprite_sel.image, (0, 0))
            self.image.fill((255, 255, 255))
        else:
            self.image.blit(self.sprite_des.image, (0, 0))
            self.image.fill((0, 0, 0))


        
        self.rect = self.sprite_sel.rect
        self.resolution = self.sprite_sel.resolution
        self.position = (position[0], position[1])
        self.position = position
        self.callout = callout
        self.attrigger = trigger
        print self.layer

    def trigger(self):
        """What state to transfer to when the button is pressed"""
        if callout == self.callout:
            return self.attrigger
        else:
            return None
        
    def update(self, callout):
        """This will set the button to deselected if it was the thing
        that is now selected, and it will make itself selected if it is"""
        if callout == self.callout:
            self.image.blit(self.sprite_sel.image, (0, 0))
            self.selected = True
            self.image.fill((255, 255, 255))
            print 'update to', self.callout
        else:
            self.image.blit(self.sprite_des.image, (0, 0))
            self.image.fill((0, 0, 0))
            self.selected = False
            print 'away from', self.callout

        super(Button, self).update()

def keys(event, action):
    """A little hack to make it easier to use the other parts of the programs, I
    think it is a little unneccecary, but it is OK, just shows how you can make
    the program take more room or something
    """
    if action == 'escape':
        if event.key == pygame.K_ESCAPE:
            return True
    elif action == 'left':
        if event.key == pygame.K_KP4 or event.key == pygame.K_LEFT:
            return True
    elif action == 'right':
        if event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT:
            return True
    elif action == 'up':
        if event.key == pygame.K_KP8 or event.key == pygame.K_UP:
            return True
    elif action == 'down':
        if event.key == pygame.K_KP2 or event.key == pygame.K_DOWN:
            return True
    elif action == 'next':
        if event.key == pygame.K_KP1 or event.key == pygame.K_KP3 or event.key == pygame.K_SPACE:
            return True
    elif action == 'back':
        if event.key == pygame.K_KP7 or event.key == pygame.K_KP5 or event.key == pygame.K_x:
            return True
    else:
        return False

class AnyMenu(SubGame):
    """Extend this for any menu"""
    def __init__(self, arg):
        super(AnyMenu, self).__init__()
        self.arg = arg

    def transition_in(self):
        """Dummy"""
        pass

    def allign(self, allign):
        """Setup the alligment graphic"""
        
        
    def main_loop(self, list):
        self.t = self.t + 1
        self.group.draw()
        GetScreen().draw()
        #Handle Other Events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if (keys(event, 'up') and
                  ('U' in list[self.cursor[0]][self.cursor[1]][1])):
                    self.cursor[0] -= 1
                    self.group.update(mainmen[self.cursor[0]][self.cursor[1]][0])
                elif (keys(event, 'down') and
                  ('D' in list[self.cursor[0]][self.cursor[1]][1])):
                    self.cursor[0] += 1
                    self.group.update(mainmen[self.cursor[0]][self.cursor[1]][0])
                elif (keys(event, 'left') and
                  ('L' in list[self.cursor[0]][self.cursor[1]][1])):
                    self.cursor[1] -= 1
                    self.group.update(mainmen[self.cursor[0]][self.cursor[1]][0])
                elif (keys(event, 'right') and
                  ('R' in list[self.cursor[0]][self.cursor[1]][1])):
                    self.cursor[1] += 1
                    self.group.update(mainmen[self.cursor[0]][self.cursor[1]][0])
                elif event.key == K_ESCAPE:
                    self.pop_state()
                elif event.key == K_RETURN:
                    self.pop_state()

                        



###Classes for Menus###
class MainMenu(AnyMenu):
    """Class for the instruction pages"""
    def __init__(self):
        super(MainMenu, self).__init__(self)
        self.initialized = False

    def transition_in(self):
        #General initialization
        if self.initialized:
            return
        self.cursor = [0, 0]
        self.initialized = True
        self.set_layers(['main'])
        self.t = 0        
        #Background initialization
        bg = load_image(os.path.join('data', 'spacebg.jpg'))
        self.screen_state.set_background(bg)
        #Font & text initialization
        pygame.font.init()
        self.font = pygame.font.SysFont(None,80)
        

        #Sprite initialization
#       self.play = Button(   sel_svg = main_play_sel, SVG for selected
#                             des_svg = main_play_des, SVG for deselected
#                             size = ( None, 50 ),     Starting Size
#                             callout = 'play',        Name to respond to
#                             initsel = True,          Start selected?
#                             trigger = None)          What to launch on click


        self.play = Button(   sel_svg = main_play_sel,
                              des_svg = main_play_des,
                              size = ( None, 50 ),
                              callout = 'play',
                              initsel = True,
                              trigger = None)
        self.howto = Button(  sel_svg = main_play_sel,
                              des_svg = main_play_des,
                              size = ( None, 50 ),
                              callout = 'how',
                              initsel = False,
                              trigger = None)
        self.about = Button(  sel_svg = main_play_sel,
                              des_svg = main_play_des,
                              size = ( None, 50 ),
                              callout = 'about',
                              initsel = False,
                              trigger = None)
        self.credits = Button(sel_svg = main_play_sel,
                              des_svg = main_play_des,
                              size = ( None, 50 ),
                              callout = 'cred',
                              initsel = False,
                              trigger = None)

        positions = []
        sw, sh = self.screen_state.get_size()
        
        self.play.rect.midtop = (sw/2, int(sh*.25))
        self.howto.rect.midtop = (sw/2, int(sh*.39))
        self.about.rect.midbottom = (sw/2, int(sh-(sh*.17)))
        self.credits.rect.midbottom = (sw/2, int(sh-(sh*.05)))

        print self.play.rect.midtop
        print self.howto.rect.midtop
        print self.about.rect.midbottom
        print self.credits.rect.midbottom


        #Sprite group initialization
        self.group = Group(self.play, self.howto, self.about, self.credits)

    def main_loop(self):
        """Run the main loop"""
        super(MainMenu, self).main_loop(mainmen)

        for event in pygame.event.get():
            if keys(event, 'next'):
                for sprite in self.group.sprites():
                    trigger = sprite.trigger()
                    if trigger is not None:
                        self.newstate = trigger()
                        self.newstate.push_state()



            

