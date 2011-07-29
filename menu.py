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

import run
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
##  For the Char Menu                    ##
###########################################

charmen = (
           (('python','D'),),
           (('tux',  'UD'),),
           (('gnu',  'UD'),),
           (('wilber','U'),)
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
class Allignment(Sprite):
    """A simple SVG background allignment"""
    def __init__(self, svg=None, size=None):
        super(Allignment, self).__init__()
        self.svg = svg
        data = open(svg).read()
        self.sprite = svgsprite.SVGSprite(svg=data, size=size)
        self.image = self.sprite.image 
        self.rect = self.sprite.rect
        self.resolution = self.sprite.resolution
        self.position = (0, 0)
        self.layer = 'allignment'

    def update(self, *args):
        """do nothing"""
        pass
    
    def trigger(self, *args):
        pass
        

class Button(Sprite):
    """Base button class to be built upon"""
    def __init__(self, position = (0, 0), #starting position?
                 sel_svg=None, des_svg=None, # images
                 size=None, # only spec the vertical/hor size
                 callout='NO', # Name to respond to select
                 initsel=False, # Select this on start
                 trigger=[None, None]):  # what should be done on a trigger
        
        data_sel = open(sel_svg).read()
        data_des = open(des_svg).read()
        self.sprite_sel = svgsprite.SVGSprite(svg=data_sel, size=size)
        self.sprite_des = svgsprite.SVGSprite(svg=data_des, size=size)

        self.selected = initsel
        Sprite.__init__(self)
        if self.selected is True:
            self.image = self.sprite_sel.image
        else:
            self.image = self.sprite_des.image
        
        self.rect = self.sprite_sel.rect
        self.resolution = self.sprite_sel.resolution
        self.position = (position[0], position[1])
        self.position = position
        self.callout = callout
        self.attrigger, self.triggersender = trigger

    def trigger(self, callout):
        """What state to transfer to when the button is pressed"""
        if callout == self.callout:
            return (self.attrigger, self.triggersender)
        else:
            return None
        
    def update(self, callout):
        """This will set the button to deselected if it was the thing
        that is now selected, and it will make itself selected if it is"""
        if callout == self.callout:
            self.image = self.sprite_sel.image
            self.selected = True
        else:
            self.image = self.sprite_des.image
            self.selected = False

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
###########################################################################
# Basic Menu to Extend                                                    #
###########################################################################

class AnyMenu(SubGame):
    """Extend this for any menu"""
    def __init__(self, arg):
        super(AnyMenu, self).__init__()
        self.arg = arg

    def transition_in(self):
        """Do things for every menu"""
        self.cursor = [0, 0]        
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        self.set_layers(['main', 'allignment'])
        self.t = 0        
        #Background initialization
        bg = load_image(os.path.join('data', 'spacebg.jpg'))
        self.screen_state.set_background(bg)
        #Font & text initialization
        pygame.font.init()
        self.font = pygame.font.SysFont(None,80)
        
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
                    self.group.update(list[self.cursor[0]][self.cursor[1]][0])
                elif (keys(event, 'down') and
                  ('D' in list[self.cursor[0]][self.cursor[1]][1])):
                    self.cursor[0] += 1
                    self.group.update(list[self.cursor[0]][self.cursor[1]][0])
                elif (keys(event, 'left') and
                  ('L' in list[self.cursor[0]][self.cursor[1]][1])):
                    self.cursor[1] -= 1
                    self.group.update(list[self.cursor[0]][self.cursor[1]][0])
                elif (keys(event, 'right') and
                  ('R' in list[self.cursor[0]][self.cursor[1]][1])):
                    self.cursor[1] += 1
                    self.group.update(list[self.cursor[0]][self.cursor[1]][0])
                elif event.key == K_ESCAPE:
                    self.pop_state()
                    return
                elif keys(event, 'next'):
                    if list[self.cursor[0]][self.cursor[1]][0] != 'none':
                        for sprite in self.group.sprites():
                            trigger = sprite.trigger(list[self.cursor[0]][self.cursor[1]][0])
                            if trigger is not None:
                                trigger[1].triggers(trigger[0])
                                return
                elif keys(event, 'back'):
                    self.pop_state()
                    return
                            
######################################################################
# GRADE MENU                                                         #
######################################################################
class GradeMenu(AnyMenu):
    """Class for the instruction pages"""
    def __init__(self):
        super(GradeMenu, self).__init__(self)
        self.initialized = False

    def transition_in(self):
        #General initialization
        if self.initialized:
            return
        super(GradeMenu, self).transition_in()
        self.initialized = True

        

        #Sprite initialization
#       self.play = Button(   sel_svg = main_play_sel, SVG for selected
#                             des_svg = main_play_des, SVG for deselected
#                             size = ( None, 50 ),     Starting Size
#                             callout = 'play',        Name to respond to
#                             initsel = True,          Start selected?
#                             trigger = None)          What to launch on click

        
        self.resume = Button( sel_svg = grades_resume_sel,
                              des_svg = grades_resume_des,
                              size = ( 750, None ),
                              callout = 'resume',
                              initsel = True,
                              trigger = [CharecterMenu, self])
                              
        self.first = Button(  sel_svg = grades_1_sel,
                              des_svg = grades_1_des,
                              size = ( 275, None ),
                              callout = 'first',
                              initsel = False,
                              trigger = [None, self])
                              
        self.second = Button( sel_svg = grades_2_sel,
                              des_svg = grades_2_des,
                              size = ( 275, None ),
                              callout = 'second',
                              initsel = False,
                              trigger = [None, self])
                              
        self.third = Button(  sel_svg = grades_3_sel,
                              des_svg = grades_3_des,
                              size = ( 275, None ),
                              callout = 'third',
                              initsel = False,
                              trigger = [None, self])

        positions = []
        sw, sh = self.screen_state.get_size()
        
        self.resume.rect.midtop = (sw/2, int(sh*.2))
        self.second.rect.midtop = (sw/2, int(sh*.36))
        self.first.rect.midright =  (int(self.second.rect.midleft[0] - (sw*.01)),
                                     self.second.rect.midleft[1])
        self.third.rect.midleft  =  (int(self.second.rect.midright[0] + (sw*.01)),
                                     self.second.rect.midright[1])

        
        self.allignment = Allignment(svg=grades_allign, size = (0, sh))
        self.allignment.rect.midtop = (sw/2, 0)

        #Sprite group initialization
        self.group = Group(self.resume, self.first, self.second, self.third,
                           self.allignment)

    def main_loop(self):
        """Run the main loop"""
        super(GradeMenu, self).main_loop(grades)
        
    def triggers (self, trigger):
        """ Callback for trigger usage """
        if trigger is not None:
            self.newstate = trigger()
            self.newstate.push_state()
            return
        
######################################################################
# Charecter MENU                                                     #
######################################################################
class CharecterMenu(AnyMenu):
    """Class for the instruction pages"""
    def __init__(self):
        super(CharecterMenu, self).__init__(self)
        self.initialized = False

    def transition_in(self):
        #General initialization
        if self.initialized:
            return
        super(CharecterMenu, self).transition_in()
        self.initialized = True

        #Sprite initialization
#       self.play = Button(   sel_svg = main_play_sel, SVG for selected
#                             des_svg = main_play_des, SVG for deselected
#                             size = ( None, 50 ),     Starting Size
#                             callout = 'play',        Name to respond to
#                             initsel = True,          Start selected?
#                             trigger = None)          What to launch on click

        
        self.snake = Button(  sel_svg = charecter_python_sel,
                              des_svg = charecter_python_des,
                              size = ( 400, None ),
                              callout = 'python',
                              initsel = True,
                              trigger = ['python', self])
                              
        self.tux = Button(  sel_svg = charecter_tux_sel,
                              des_svg = charecter_tux_des,
                              size = ( 450, None ),
                              callout = 'tux',
                              initsel = False,
                              trigger = ['tux', self])
                              
        self.gnu = Button( sel_svg = charecter_gnu_sel,
                              des_svg = charecter_gnu_des,
                              size = ( 530, None ),
                              callout = 'gnu',
                              initsel = False,
                              trigger = ['gnu', self])
                              
        self.wilber = Button(  sel_svg = charecter_wilber_sel,
                              des_svg = charecter_wilber_des,
                              size = ( 610, None ),
                              callout = 'wilber',
                              initsel = False,
                              trigger = ['wiber',self])

        positions = []
        sw, sh = self.screen_state.get_size()
        
        self.snake.rect.midtop= (sw/2, int(sh*.25))
        self.tux.rect.midtop  = (sw/2, int(sh*.39))
        self.gnu.rect.midbottom = (sw/2, int(sh - (sh*.17)))
        self.wilber.rect.midbottom = (sw/2, int(sh - (sh*.05)))


        
        self.allignment = Allignment(svg=charecter_allign, size = (0, sh))
        self.allignment.rect.midtop = (sw/2, 0)

        #Sprite group initialization
        self.group = Group(self.snake, self.tux, self.gnu, self.wilber,
                           self.allignment)

    def main_loop(self):
        """Run the main loop"""
        super(CharecterMenu, self).main_loop(charmen)
        
    def triggers (self, trigger):
        """ Callback for trigger usage """
        self.newstate = run.PlayState(trigger, 'none', 'none')
        self.newstate.push_state()
        return
        

######################################################################
# How to Menu                                                        #
######################################################################
class HowToMenu(AnyMenu):
    """Class for the instruction pages"""
    def __init__(self):
        super(HowToMenu, self).__init__(self)
        self.initialized = False

    def transition_in(self):
        #General initialization
        if self.initialized:
            return
        super(HowToMenu, self).transition_in()
        self.initialized = True

        self.allignment = Allignment(svg=htpl_allign, size = (0, sh))
        self.allignment.rect.midtop = (sw/2, 0)

        #Sprite group initialization
        self.group = Group(self.allignment)

    def main_loop(self):
        """Run the main loop"""
        super(HowToMenu, self).main_loop(how)
        
    def triggers (self, trigger):
        """ Callback for trigger usage """
        if trigger is not None:
            self.newstate = trigger()
            self.newstate.push_state()
            return
            
######################################################################
# Main Menu                                                          #
######################################################################
class MainMenu(AnyMenu):
    """Class for the instruction pages"""
    def __init__(self):
        super(MainMenu, self).__init__(self)
        self.initialized = False

    def transition_in(self):
        #General initialization
        if self.initialized:
            return
        super(MainMenu, self).transition_in()
        self.initialized = True

        

        #Sprite initialization
#       self.play = Button(   sel_svg = main_play_sel, SVG for selected
#                             des_svg = main_play_des, SVG for deselected
#                             size = ( None, 50 ),     Starting Size
#                             callout = 'play',        Name to respond to
#                             initsel = True,          Start selected?
#                             trigger = None)          What to launch on click

        
        self.play = Button(   sel_svg = main_play_sel,
                              des_svg = main_play_des,
                              size = ( 350, None ),
                              callout = 'play',
                              initsel = True,
                              trigger = [GradeMenu, self])
                              
        self.howto = Button(  sel_svg = main_howto_sel,
                              des_svg = main_howto_des,
                              size = ( 562, None ),
                              callout = 'how',
                              initsel = False,
                              trigger = [HowToMenu, self])
                              
        self.credits = Button(sel_svg = main_credits_sel,
                              des_svg = main_credits_des,
                              size = ( 312, None ),
                              callout = 'cred',
                              initsel = False,
                              trigger = [None, self])
                              
        self.about = Button  (sel_svg = main_about_sel,
                              des_svg = main_about_des,
                              size = ( 312, None ),
                              callout = 'about',
                              initsel = False,
                              trigger = [None, self])

        positions = []
        sw, sh = self.screen_state.get_size()
        
        self.play.rect.midtop = (sw/2, int(sh*.25))
        self.howto.rect.midtop = (sw/2, int(sh*.39))
        self.credits.rect.midbottom = (sw/2, int(sh - (sh*.17)))
        self.about.rect.midbottom = (sw/2, int(sh - (sh*.05)))

        self.allignment = Allignment(svg=main_allign, size = (0, sh))
        self.allignment.rect.midtop = (sw/2, 0)

        #Sprite group initialization
        self.group = Group(self.play, self.howto, self.about, self.credits,
                           self.allignment)

    def main_loop(self):
        """Run the main loop"""
        super(MainMenu, self).main_loop(mainmen)
        
    def triggers (self, trigger):
        """ Callback for trigger usage """
        if trigger is not None:
            self.newstate = trigger()
            self.newstate.push_state()
            return

