#!/usr/bin/env python
# Space Math
# Copyright (C) 2011 Mark Amber and Lucas Morales
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
#Import APH libraries
from APH import *
from APH.Game import *
from APH.Utils import *
from APH.Screen import *
from APH.Sprite import *

import olpcgames
import pygame
import logging 
from olpcgames import pausescreen, textsprite, svgsprite
from egen import egen as egen
from egen import answergen as answergen
from random import *
import os
import panglery
from gamemanager import *
import printer
import questions.getquestion
log = logging.getLogger( 'HelloPygame run' )
log.setLevel( logging.DEBUG )
import menu
import assets
import config


class MaskSprite(Sprite):
    """ A sprite superclass which adds automatic generation of masks for
    the sprite as they are needed. """
    def __setattr__(self, item, value):
        if item == 'image':
            if 'mask' in self.__dict__:
                self.__dict__.pop('mask')
            Sprite.__setattr__(self, item, value)
        else:
            Sprite.__setattr__(self, item, value)
            
    def __getattr__(self, item):
        if item == 'mask':
            if 'mask' not in self.__dict__:
                self.__dict__['mask'] = pygame.mask.from_surface(self.image)
            return self.__dict__['mask']
        else:
            return Sprite.__getattr__(self, item)

def my_load_image(imgName,colorkey=None):
    newName = os.path.join('data',imgName)
    return load_image(newName,colorkey)

        

class MovingTextObject(textsprite.TextSprite):

    """Moving Text Object extends TextSprite to allow it to move.

    Use it just like a TextSprite except its update method has something to move
    it around
    
    """

    def __init__(self, text=None, family=None, size=None, bold=False,
                 italic=False, color=None, background=None):

        super(MovingTextObject, self).__init__(text, family, size,
                                        bold, italic, color,
                                        background)
        self.change_y = 0
        self.change_x = 0

    def changespeed(self, x, y):
        """Change the speed of the text"""
        # @x add speed to the x direction
        # @y add speed to the y direction
        self.change_x+=x
        self.change_y+=y
        
    # Update the location
    def update(self):
        """Remap the new position of the text"""
        self.rect.top += self.change_y
        self.rect.left += self.change_x
        super(MovingTextObject, self).update()

class MovingSvgObject(MaskSprite):

    """Moving SVG Object extends SVGSprite to allow it to move.
    
    Use it the same way you would ues an SVGSprite
    
    """

    def __init__(self, position = (0, 0), svg=None, size=None, copy=False):

        if copy is not False and copy.__class__ == svgsprite.SVGSprite:
            self.sprite = copy.copy()
        else:
            data = open(svg).read()
            self.sprite = svgsprite.SVGSprite(svg=data, size=size)

        super(MovingSvgObject, self).__init__()
        
        #==================
        # Setup init values
        self.image = new_surface(self.sprite.image.get_size())
        self.image.blit(self.sprite.image, (0, 0))
        self.rect = self.sprite.rect
        self.resolution = self.sprite.resolution
        self.position = (position[0], position[1])
        self.change_x = 0
        self.change_y = 0
        self.layer = 'test'
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




class ExclaimMessage(Sprite):
    """Show something on the screen"""
    def __init__(self, gm):
        super(ExclaimMessage, self).__init__()
        self.gm = gm

        #================
        # New empty image
        self.empty = new_surface((350, 100))
        self.image = self.empty
        self.rect = self.image.get_rect()
        self.group = self.gm.messages_group # Get the correct Group from GM
        self.add(self.group) # Add to our own group
        self.rect.midbottom = (self.gm.size[0]/2, self.gm.size[1]) #set to bottom mid of screen
        
        #=========================================
        # Init some images for predefined messages
        self.correct = StaticSVG(svg=assets.correct, size=(350, None))
        self.incorrect = StaticSVG(svg=assets.incorrect, size=(350, None))
        self.great_job = StaticSVG(svg=assets.great_job, size=(350, None))
        self.ouch = StaticSVG(svg=assets.ouch, size=(350, None))
        
        #======================================================
        # Setup ticker and displaying and cue for update method
        self.ticker = 0
        self.displaying = False
        self.que = [] # Messages will go in the que

        #++++++++++++++++++++++
        # Hook for life lost
        @self.gm.p.subscribe(event='message', needs=['message'])
        def message_hook(p, message):
            self.exclaim(message)
        #----------------------

    def exclaim(self, message):
        #=============================
        # Cases for different messages
        if message == 'incorrect':
            self.que.append(self.incorrect.image)
        elif message == 'correct':
            self.que.append(self.correct.image)
        elif message == 'good_job':
            self.que.append(self.great_job.image)
        elif message == 'ouch':
            self.que.append(self.ouch.image)

    def update(self):
        """Update the message and play all in que"""
        #=========================================
        # If the ticker is out at the que is full:
        if self.ticker <= 0 and len(self.que) > 0:
            self.image = self.que.pop(-1) # Set the image to the next in line
            self.ticker += 15 # Refill the ticker
            self.displaying = True # Set a temp variable becuse we are displying
        #===============================================
        # If the ticker is expired and there are no more
        # things left in the que
        elif self.ticker <= 0:
            #=============================
            # If we have something showing
            if self.displaying == True:
                self.image = self.empty # Blank the message
                self.displaying = False # Set temp variable back to False
        #============================
        # If the ticker is still full
        elif self.ticker > 0:
            self.ticker -= 1 # Drain the ticker
        #================================
        # We must be displaying a message
        else:
            pass #currently showing a message
        
        

class StaticSVG(Sprite):
    """A simple static SVG"""
    def __init__(self, svg=None, size=None):
        super(StaticSVG, self).__init__()
        self.svg = svg

        #==================================
        # Open svg and set it to the sprite
        data = open(svg).read()
        self.sprite = svgsprite.SVGSprite(svg=data, size=size)
        self.image = self.sprite.image 
        self.rect = self.sprite.rect
        self.resolution = self.sprite.resolution
        self.position = (0, 0)

    def update(self, *args):
        """do nothing"""
        pass



class LifeManager(object):

    """Manage life"""

        
    def __init__(self, gm):
        self.gm = gm
        super(LifeManager, self).__init__()

        #======================
        # Size of square hearts
        self.imagesize = 30
        
        #===============================
        # Setup images for little hearts
        self.full = StaticSVG(svg=assets.life_full, size=(self.imagesize, None))
        self.empty = StaticSVG(svg=assets.life_empty, size=(self.imagesize, None) )
        
        self.group = self.gm.life_group

                
        #================================
        # The relates how many lives with
        # the picture of each life
        f = self.full
        e = self.empty
        self.map = [[e, e, e],  # No Lives left
                    [f, e, e],  #  1 Lives left
                    [f, f, e],  #  2 Lives left
                    [f, f, f]]  #  3 Lives left

        #=============================================
        # Lists and things for running of life manager
        self.lifeblips = []
        self._lives = 3
        self.ticker = 0

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Hook for life lost
        @self.gm.p.subscribe(event='life_lost', needs=['scope'])
        def example_hook(p, scope):
            self.loose(scope)
        #--------------------------------------------------------

        #===============================
        # Add a little heart three times
        for i in range(3):
            self.lifeblips.append(StaticSVG(svg=assets.life_full,
                                            size=(self.imagesize, None)))
            
            self.lifeblips[-1].rect.topleft = ( # Get the latest entry
                                                ( ((i + 1) * 5) + ((i + 1) * 
                                                                   self.imagesize) ),
                                               # (above) add margin for each   #
                                               # and compensate for image size #
                                               #===============================#
                                               # (below) put them 5 pixils from#
                                               # the bottom of the screen      #
                                                (self.gm.size[1] -
                                                 self.imagesize - 5)
                                              )
        
        self.group.add(*self.lifeblips) # Add all the little heats to the group

        self.lives = 3 # This is unneccecary, but set current lives to 3

    #=======================================================
    # Called when a life is lost, assesses the situation and
    # does the right action depending on why it was lost
    def loose(self, scope):
        #==============
        # You were shot
        if scope == 'shot':
            self.lives -= 1
        #=================
        # Enemy slipped by
        elif scope == 'slipped':
            #=======================
            # if the ticker is empty
            if self.ticker <= 0:
                self.lives -= 1
                # Loose a life
            self.ticker += 40
            # and fill the ticker
            # The ticker keeps the
            # enemys from loosing you
            # a life each time. 
        #=========================
        # You answered incorrectly
        elif scope == 'incorrect':
            self.lives -= 1
            # Just remove a life

    #=============================
    # getter for the life property
    def get_lives(self):
        """get the current number of lives"""
        return self._lives
    
    #=============================
    # setter for the life property
    def set_lives(self, value):
        """Set number of lives and update the screen"""
        self._lives = value
        #=======================
        # If we are not dead yet
        if not self._lives < 0:
            #=============================
            # for each little life picture
            for minilife, life in zip(self.map[self._lives], self.lifeblips):
                life.image = minilife.image # Set them according to the map
        #===============
        # If we are dead
        else:
            self.gm.p.trigger(event='end_game', clean=False)
            # Signal the end of game, with an unclean finish
    
    #=======================
    # Called for every frame
    def update(self):
        """ Add the time to the ticker in case something needs to happen
        with the life looser
        """
        #===========================
        # if the ticker is not empty
        if self.ticker > 0:
            self.ticker -= 1
            # tock the ticker
        self.group.update()
        # Update the group
    
    #=========
    # Property
    lives = property(get_lives, set_lives)

############ THE ENEMYS #######################################################        

class Enemy(MovingSvgObject):
    
    """Enemy is the basic non-friendly thing in the game
        
        An Enemy is something in general that you want to shoow, although if it is a
        wrong answer it is something that you do not want to shoot, but in any case
        still some remain that you do want to shoot
        
        """
    
    def __init__(self, size, svg, position, speed = config.speed, copy = False):
        self.pos = position
        self.siz = size
        super(Enemy, self).__init__(position = self.pos, svg = svg, size =
                                    self.siz, copy = copy)
        self.change_x = speed
    
    def update(self):
        """This just passes the update up the line"""
        super(Enemy, self).update()            
            
class AnswerGuy(MaskSprite):
    
    """Answer guy extends Enemy, you can shoot it to solve a problem
    
    the correct argument is important because it allows the answerguy to know
    what it should do to you when it is hit, also you need to pass it something
    to write on itself
    
    """
    
    def __init__(self, position, size, friendly_bulletgroup, friendly_player,
                 correct,  gm, response, copy =  False):

        #================================
        # set the values from initisation
        self.pos = position
        self.siz = size
        self.friendly_bulletgroup = friendly_bulletgroup
        self.gm = gm
        self.correct = correct
        self.text = response

        #===================================
        # Check to see if we have a copy SVG
        if copy is not False and copy.__class__ == svgsprite.SVGSprite:
            self.svg = copy.copy()
            # Use that copy for our svg
        #==================================
        # if we were not given a valid copy
        else:
            self.data = open(os.path.join("data", "numenemy.svg")).read()
            self.svg = svgsprite.SVGSprite(svg = self.data,
                                           size = self.siz)
            # Open our SVG and set it to our svg

                super(AnswerGuy, self).__init__()
        self.change_x = config.speed # Speed in x, set to setting in config file
        self.change_y = 0

        #=============================
        # Create our sprite attributes
        self.image = new_surface(size)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.position = (self.pos[0], self.pos[1])
        
        self.image.blit(self.svg.image, (0, 0))
        self.image.blit(self.text.image, (self.siz[0] / 3, self.siz[1] / 3))
        # Blit our svg background, then the right/wrong answer on top
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.friendly_player = friendly_player

    def update(self):
        """This will update the Answers, change their direction, stuff like
        that, it will also see if they have been hit, in that case if it is a
        correct answer will call for you to go on to the next level, and in the
        case that it is an incorrect answer will do that plus show the correct
        answer on the screen then subtract a life.
        """
        #====================================
        # Find all the colisions with bullets
        collisions = pygame.sprite.spritecollide(self,
                                                 self.friendly_bulletgroup,
                                                 True,
                                                 pygame.sprite.collide_mask)
        #=====================
        # if we were just shot
        if len(collisions) > 0:
            self.gm.p.trigger(event='shot_answer', correct=self.correct)
            self.kill()
        self.rect.top += self.change_y
        self.rect.left += self.change_x
        
        #=================================
        # If the guys have left the screen
        if self.rect.left < -100:
            self.kill()
            self.gm.p.trigger(event='life_lost', scope='slipped')

        super(AnswerGuy, self).update()

class BadGuy(Enemy):

    """A BadGuy is a simple enemy, it only can be destroyed or destroy you.

    The BadGuy will shoot you when you are in its path, but will only shoot
    again once you have cleared and reentered its path, so stay out of its way!
    
    """
    def __init__(self, position, size, friendly_bulletgroup,
                 opponent_bulletgroup, bullets, friendly_player, gm, copy = False):
        # @position position to start at
        # @size iterable size
        # @friendly_bulletgroup the bullet group that is shooting at it
        # @bullets a list of bullets, unused, for some reason
        # @friendly_player the player
        # @the game manager
        # @copy is this a copy, if so give it one
        #==================
        # Setup init values
        self.pos = position
        self.siz = size
        self.friendly_bulletgroup = friendly_bulletgroup
        self.opponent_bulletgroup = opponent_bulletgroup
        self.bullets = []
        self.gm = gm
        super(BadGuy, self).__init__(position = self.pos, size = self.siz,
                                     svg = os.path.join('data', 'enemy2.svg'),
                                     copy = copy)
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.friendly_player = friendly_player
        self.onefire = False
        self.bullet_offset = (0, 0)

    def update(self):
        """This will update the BadGuy and change its direction and fire if
        something is in its way, it will also check to see if it is hit and
        destroy itself if that is the case.
        """
        #===============================================
        # Check for collisions with the good bulletgroup
        collisions = pygame.sprite.spritecollide(self,
                                                 self.friendly_bulletgroup,
                                                 True,
                                                 pygame.sprite.collide_mask)
        #===============
        # If it was shot
        if len(collisions) > 0:
            self.kill()
            self.gm.p.trigger(event='strays', bulletlist = self.bullets,
                            bulletgroup = self.opponent_bulletgroup)

        super(BadGuy, self).update()
        
        #==============================================================
        # If the player is just coming in view and is not there already
        if ((self.rect.midleft[1] >= self.friendly_player.rect.topright[1])
        and (self.rect.midleft[1] <= self.friendly_player.rect.bottomright[1])
        and (self.rect.midleft[0] < self.gm.size[0] - 30)):
            if self.onefire == False:
                self.bullets.append(BadBullet((self.rect.midleft[0] +
                                               self.bullet_offset[0],
                                               self.rect.midleft[1] +
                                               self.bullet_offset[1])))
                self.opponent_bulletgroup.add(self.bullets[-1])
                self.onefire = True
        else:
            self.onefire = False

        #==========================
        # if we have left the stage
        if self.rect.left < -100:
            self.kill()
            self.gm.p.trigger(event='strays', bulletlist = self.bullets,
                            bulletgroup = self.opponent_bulletgroup)
            self.gm.p.trigger(event='life_lost', scope='slipped')

        #===========================================
        # pop the bullets if they are off the screen
        for i in self.bullets:
            if i.rect.left < -20:
                i.remove(self.opponent_bulletgroup)
                self.bullets.remove(i)

class StrayBulletManager(object):
    """Cleans up stray bullets left behind by enemies that have died
        
        A pangler trigger is used to signal this class that it should be monitoring
        stray bullets for a perticular bullet list. Pass a list of bullets along
        with the panglery trigger and let the stray bullet manager update and
        monitor the positions of the lost bullets. after a list of bullets is fully
        depleted, the list will be removed from the que
        
        """
    
    def __init__(self, gm):
        
        #==================
        # setup init values
        self.straylists = []
        self.gm = gm
        
        #+++++++++++++++++++++++++++++++++
        # Hook for stray bullet management
        @self.gm.p.subscribe(event='strays', needs=['bulletlist', 'bulletgroup'])
        def strays_hook(p, bulletlist, bulletgroup):
            self.straylists.append([bulletlist, bulletgroup])
        #---------------------------------
        
    def update(self):
        """Update the lists of stray bullets"""
        
        #=============================
        # for each of the bullet lists
        for i in self.straylists:
            #========================
            # for each of the bullets
            for g in i[0]:
                #========================
                # if they left the screen
                if g.rect.left < -25:
                    g.remove(i[1])
                    i[0].remove(g)
                    # Remove them from the
                    # list and the screen

###### THIS IS THE MOST AMAZING CLASS EVER ###################################

class LaserCannon(Sprite):

    """The LaserCannon is a high tech wepon system on your vehical
    
    It is best to think of the LaserCannon as a machine, rather than the thing
    in the corner that it actually represents, think of that as the front end to
    it, and the back end is whatever is in the vehical shooting the energy

    The LaserCannon controls:
        - Cannon fireing overload (in the form of overheating)
        - All friendly lasers on the field
        - Removing stray laser energy to improve CPU
        - Catalouging all laser energy locations
        - Displays the temperature on the screen
        - Noises when laser cannon capacitors discharge

    The lasercannon is the core part of the game since it allows bullets to be
    fired to answer questions and destroy other targets
    
    Be carefull when shooting with the LaserCannon to avoid overheating, the
    components can get hot, and when that happens a failsafe mode is activated
    to prevent further damage to the Lasercannon, that is called overheated, and
    when it is true you will have to wait for the heat to get back to 0

    Speaking of heat, as with all matter, this follows the accepted laws of
    physics, since heat will always try to reach thermodynamic equilibriam, a
    cold space like deep space will allow the laser cannon to cool down quite
    fast, it only takes 3 seconds for the cannon to cool down after an overheat,
    because:
        - game runs 25 fps
        - lasercannon cools 1 degree every frame)
        - 75 frames to cool down / 25 fps = 3 seconds

    """
    
    def __init__(self, gm):
        self.gm = gm
        Sprite.__init__(self)
        self.sounds = []
        self.offset = gm.player_cannon_offset
        
        #======================================
        # add sound objects to a list of sounds
        self.sounds.append(pygame.mixer.Sound(assets.laser1))
        self.sounds.append(pygame.mixer.Sound(assets.laser2))
        self.sounds.append(pygame.mixer.Sound(assets.laser3))
        
        #======================
        # finish initialization
        self.bulletgroup = gm.friendly_bullet_group
        self.blackness = new_surface([75, 15])
        self.blackness.fill((0, 0, 0))
        self.redness = new_surface([75, 15])
        self.image = new_surface([75, 15])
        self.redness.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
        self.overheated = False
        self.heat = 0
        self.bullets = gm.playable_bullets

    def overheat(self):
        """Overheat the cannon and max the heat"""
        self.overheated = True
        self.heat = 75

    def shoot(self, position):
        """Causes the LaserCannon to discharge one blast of electron radiation"""
        if self.overheated == False:
            # LaserCannon will only fire if it is at a safe temperature
            self.bullets.append(FriendlyBullet((position[0] + self.offset[0],
                                               position[1] + self.offset[1])))
            # Create a new 'bullet'
            self.heat += 20
            # increse the heat of the LaserCannon
            self.bulletgroup.add(self.bullets[-1])
            # Add the newly created 'bullet' to the sprite group
            choice(self.sounds).play()
            # Randomly select one of the sounds from the list created earlier
            if self.heat >= 75:
                self.overheat()
                # If applicable, overheat the lasercannon

    def color_finder(self, heat):
        """Perform a linear equation to find the color of the bar
        00-25 color is green
        26-50 color is from green-yellow
        51-75 color is yellow-red

        Think of lines with slope 10.2, that way they have 255 rise for 25 run
            ______
        255    /\
        0   __/  \ 75  The spike is the red first going up and the green down

        """
        self.heat = heat
        if heat <= 25:
            return (0, 255, 0)
        elif heat <= 50:
            self.red = (10.2 * self.heat) - 255
            return (self.red, 255, 0)
        elif heat <= 75:
            self.green = 765 - (10.2 * self.heat)
            return (255, self.green, 0)
        else:
            return (255, 255, 255)


    def update(self):
        """Update will remove any stray bullets, and change the temperature down
        every tick, as well as display the temperature in the corner of the
        screen
        """
        #================================
        # if the heat is greater than one
        if self.heat > 0:
            self.heat -= 1
        #=================================
        # if it just happens to be at zero
        # and the overheated alarm is on
        elif self.overheated == True:
            self.overheated = False
            
        
        #==============================
        # if the overheated alarm is on
        if self.overheated:
            self.redness.fill((255, 0, 0))
        #====================
        # if it is all normal
        else:
            self.redness.fill(self.color_finder(self.heat))
            
        #===========================
        # Refresh the image
        self.image = new_surface([75, 15])
        self.image.blit(self.redness, (0, 0, self.heat, 15))
        self.image.blit(self.blackness, (self.heat, 0, 75 -
                                         self.heat, 0)) 
        #===================================
        # for each of the bullets in th list
        for i in self.bullets:
            #==================================
            # if the bullets are off the screen
            if i.rect.left > self.gm.size[0]:
                i.remove(self.bulletgroup)
                self.bullets.remove(i)

        super(LaserCannon, self).update()




############ PLAYERS ###########################################################

class Player(MovingSvgObject):
    
    """Player is the generic player, it should be extended by a type of player
    
    The player will respond when it is hit by an enemy bullet, or an enemy, but
    that is about it besides doing what all other Moving SVG objects do
    
    """
    
    def __init__(self, svg, lasercannon, size, gm):
        super(Player, self).__init__(position = (10, 10), svg = svg, size =
                                     size)
        # @svg the icon of the player
        # @lasercannon the lasercannon object
        # @size an iterable size
        # @gm the game manager
        
        #==================
        # setup init values
        self.cannon = lasercannon
        self.gm = gm
        
    def shoot(self, position):
        """This will make the plater shoot"""
        self.cannon.shoot(position)

    def update(self):
        """This is an extention of the update that is used for the movind
        object
        """
        #===========================================
        # get a list of collisions with the opponent
        collisions = pygame.sprite.spritecollide(self,
                                                 self.opponent_bulletgroup,
                                                 True,
                                                 pygame.sprite.collide_mask)
                                                 
        #=========================================
        # if we have any collisions with the enemy
        if len(collisions) > 0:
           self.gm.p.trigger(event='life_lost', scope='shot')
           
        super(Player, self).update()

        
class FlyingSaucer(Player):
    
    """Flying saucer is the vehical of choice for your favorite python.
    
    This is an extention of the Player, overriding the SVG that is displayed

    """
    
    def __init__(self, gm):
        self.cannon = gm.player_cannon
        self.opponent_bulletgroup = gm.opponent_bullet_group
        super(FlyingSaucer, self).__init__(svg=assets.charecter_flying_saucer,
                                           lasercannon = self.cannon,
                                           size = (250, None), 
                                           gm = gm)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(FlyingSaucer, self).shoot(self.rect.center)

class SpaceShuttle(Player):
    
    """Space Shuttle is the vehical of choice for your favorite linux mascot.
    
    This is an extention of the Player, overriding the SVG that is displayed

    """
    
    def __init__(self, gm):
        self.cannon = gm.player_cannon
        self.opponent_bulletgroup = gm.opponent_bullet_group
        super(SpaceShuttle, self).__init__(svg=assets.charecter_classic_rocket,
                                           lasercannon = self.cannon,
                                           size = (250, None), 
                                           gm = gm)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(SpaceShuttle, self).shoot(self.rect.center)

class ClassicRocket(Player):
    
    """The Classic Rocket is the vehical of choice for your favorite gnu mascot.
    
    This is an extention of the Player, overriding the SVG that is displayed

    """
    
    def __init__(self, gm):
        self.cannon = gm.player_cannon
        self.opponent_bulletgroup = gm.opponent_bullet_group
        super(ClassicRocket, self).__init__(svg=assets.charecter_classic_rocket,
                                           lasercannon = self.cannon,
                                           size = (300, None), 
                                           gm = gm)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(ClassicRocket, self).shoot(self.rect.center)

class FighterJet(Player):
    
    """The Fighter Jet is the vehical of choice for your favorite gimp.
    
    This is an extention of the Player, overriding the SVG that is displayed

    """
    
    def __init__(self, gm):
        self.cannon = gm.player_cannon
        self.opponent_bulletgroup = gm.opponent_bullet_group
        super(FighterJet, self).__init__(svg=assets.charecter_fighter_jet,
                                           lasercannon = self.cannon,
                                           size = (250, None), 
                                           gm = gm)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(FighterJet, self).shoot(self.rect.center)

############ BULLETS ############################################################
class Bullet(MaskSprite):
    
    """A generic bullet, should be extended.
    
    A bullet is a laser charge that somehow travels slower than the speed of
    light, maybe by some sort of altered field I don't know, but it only can
    move and cannot think for itself
    
    """

    def __init__(self, pos, color, size, speed):
        MaskSprite.__init__(self)
        #==================
        # setup init values
        self.change_x = speed
        self.change_y = 0
        self.image = new_surface(size)
        self.colored = new_surface(size)
        self.colored.fill(color)
        self.image.blit(self.colored, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.top = pos[1]
        self.rect.left = pos[0]
        self.mask = pygame.mask.from_surface(self.image)
        
        #===============================
        # hack in case we are on on olpc
        if not olpcgames.ACTIVITY:
            self.mask.fill()

    def changespeed(self, x, y):
        """Change the speed of the SVG"""
        # @x add this much to the x direction
        # @y add this much to the y direction
        self.change_x+=x
        self.change_y+=y
        
    # Remap the new location of the SVG
    def update(self):
        """Update the location of the SVG"""
        self.rect.top += self.change_y
        self.rect.left += self.change_x

        super(Bullet, self).update()

 
class FriendlyBullet(Bullet):
    
    """Friendly bullet extends a bullet.
    
    The friendly bullet has a green glow, signifying its friendlyness
    it travels in the direction of the bad guys 
    
    """
    
    def __init__(self, pos, color = (0, 255, 0),
                 size = (25, 3), speed = 30):
        super(FriendlyBullet, self).__init__(pos, color, size, speed)

class BadBullet(Bullet):
    
    """Bad buller extends a bullet.
    
    The bad bullet does exactly the same thing as a friendly bullet except at
    half the speed in the opisate direction in a different color.
    
    """
    
    def __init__(self, pos, color = (255, 0, 0),
                 size = (25, 3), speed=-15):
        super(BadBullet, self).__init__(pos, color, size, speed)

###############################################################################

def keys(event, action):
    """A little hack to make it easier to use the other parts of the programs, I
    think it is a little unneccecary, but it is OK, just shows how you can make
    the program take more room or something
    
    use:
    if event.type == something:
        if keys(event, 'down'):
            do_whatever = or ()
    
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
    elif action == 'space':
        if event.key == pygame.K_KP1 or event.key == pygame.K_SPACE:
            return True
    elif action == 'next':
        if event.key == pygame.K_KP1 or event.key == pygame.K_KP3 or event.key == pygame.K_SPACE:
            return True
    elif action == 'back':
        if event.key == pygame.K_KP7 or event.key == pygame.K_KP9 or event.key == pygame.K_x:
            return True
    else:
        return False

############# THE OPPONENT #####################################################

class ComposeButton(Sprite):
    
    """SVG with an image composited on top of it
        
        Used in the question maker, 
        
        """
    def __init__(self, position = (0, 0), #starting position?
                 svg=None, # images
                 otherimage=None,  # Image
                 offset = (0, 0)):  # offset for text
        
        data_svg = open(svg).read()
        
        Sprite.__init__(self)
        #==============================
        # Put the options in the object
        self.other = otherimage
        self.size = self.other.get_size()[1] + (2*offset[1]) 
        self.sprite = svgsprite.SVGSprite(svg=data_svg, size=( None,
                                                              self.size))
        self.image = new_surface(self.sprite.image.get_size())
        self.offset = offset
        
        #==================
        # Comose the images
        self.image.blit(self.sprite.image, (0, 0))
        self.image.blit(self.other, self.offset)
        
        #===================
        # Setup the position
        self.rect = self.sprite.rect
        self.resolution = self.sprite.resolution
        self.rect.midtop = position
    
    def update(self, callout):
        """This is called whenever the group is updated"""
        
        super(ComposeButton, self).update()

class TheOpponent():
    
    """The opponent is a controller for the things that you want to shoot.
    
    The opponent contains methods for spawning enemys at any location in
    different positions. It allows the same things to be passed to every enemy
    that is created.
    
    """
    
    def __init__(self, gm):
    
        #========================================
        # init values, store to this class object
        self.gm = gm
        self.enemies = gm.opponents
        self.group = gm.opponent_group
        self.opponent_bullets = gm.opponent_bullets
        self.friendly_bullet_group = gm.friendly_bullet_group
        self.opponent_bullet_group = gm.opponent_bullet_group
        self.friendly_player = gm.player
        self.question_group = gm.question_group
        @self.gm.p.subscribe(event='shot_answer', needs=['correct'])
        def strays_hook(p, correct):
            self.question_group.empty()
            self.group.empty()


    def spawn_badguys(self, number):
        """I will make more enemys for you"""
        
        #=============
        # bad style :{
        screensize = self.gm.opponent_size
        x_offset = self.gm.opponent_xoffset
        y_offset = self.gm.opponent_yoffset
        self.size, self.positions = egen(screensize, number, x_offset, y_offset)
        
        #=========================================
        # make the master svg, less rendering time
        self.badguysvg = svgsprite.SVGSprite(open(os.path.join('data',
                                                               'enemy.svg')).read(),
                                             self.size)
                                             
        #===============================================
        # For the number of enemies we requested, make a
        # copy of the master svg and position it and 
        # add it to the group                                     
        for i in range(len(self.positions)):
            self.enemies.append(BadGuy(self.positions[i], self.size,
                                      self.friendly_bullet_group,
                                      self.opponent_bullet_group,
                                      self.opponent_bullets,
                                      self.friendly_player,
                                      self.gm,
                                      copy = self.badguysvg))
            self.group.add(self.enemies[-1])

    def spawn_answerguys(self):
        """I will make more enemys for you"""
        
        #=============
        # Bad style :P
        screensize = self.gm.opponent_size
        x_offset = self.gm.opponent_xoffset
        y_offset = self.gm.opponent_yoffset
        self.size, self.positions = answergen(x_offset, y_offset, screensize)
        
        #=========================================
        # make the master svg, less rendering time
        self.answerguysvg = svgsprite.SVGSprite(open(os.path.join('data',
                                                                  'numenemy.svg')).read(),
                                                self.size)
        self.question = printer.Converter(questions.getquestion.get(self.gm.dbfile))
        self.question.render()
        
        #===========================================================
        # add one response for each answer we get from the generator
        for i in range(len(self.positions)):
            response = choice(self.question.responses)
            self.question.responses.remove(response)
            self.enemies.append(AnswerGuy(self.positions[i], self.size,
                                          self.friendly_bullet_group,
                                          self.friendly_player,
                                          response[1],
                                          self.gm,
                                          response[0],
                                          copy = self.answerguysvg))
            self.group.add(self.enemies[-1])
        
        #==============================================
        # Add the question to the top of the screen,
        # Under the poorly worded name of questionthing
        self.questionsprite = self.question.getquestion()
        self.questionthing = ComposeButton(position = (self.gm.size[0]/2, 10), 
                                           svg=assets.question_box,
                                           otherimage=self.questionsprite.image,
                                           offset = (15, 20)
                                          )
        self.questionthing.add(self.question_group)
        

    def update(self):
        """This will update the positions of the bullets"""
        #===============================
        # If there are no oppenents left
        if len(self.group.sprites()) == 0:
            self.gm.p.trigger(event='spawn_wave')




###############################################################################

class PlayState(SubGame):
    
    def __init__(self, charecter, gameplay, dbfile='additionupto20.shelve.db',
                 gameplaylist = ['.', 'A', '_', 'E', '2', '_', 'E', '6', '_', 'E',
                           '6', '.'],
                 levelid = 1,
                 stage = 'none',):
        
        SubGame.__init__(self)
        self.initialized = False
        self.charecterselection = charecter
        self.gameplaylist = gameplaylist
        self.gp = gameplay
        self.dbfile = dbfile
        self.levelid = levelid
        self.stage = stage

    def transition_in(self):
        # This code is for the APH, to make sure that we do not transition 2
        # times
        if self.initialized:
            return
        self.initialized = True
        pygame.init()
        self.gm = GameManager()
        self.set_layers(['test'])

        #====================
        # set values from init
        self.gm.dbfile = self.dbfile
        self.gm.levelid = self.levelid
        self.gm.gameplaylist = self.gameplaylist
        self.gm.stage = self.stage
        self.gm.gp = self.gp
        
        #====================
        # setup bad guy stuff
        self.gm.opponents = []
        self.gm.opponent_group = Group()
        self.gm.opponent_bullets = []
        self.gm.opponent_bullet_group =  Group()
        
        #======================
        # setup math game stuff
        self.gm.question_group = Group()
        self.gm.life_group = Group()
        self.gm.messages_group = Group()
       
        #======================
        # friendly groups setup
        self.gm.player_group = Group()
        self.gm.playable_bullets = []
        self.gm.friend_bullets = []
        self.gm.friendly_bullet_group = Group()
        
        self.gm.size = self.screen_state.get_size()


        #====================
        # set opponent sizing
        self.gm.opponent_size = (600, 600)
        self.gm.opponent_yoffset = (self.gm.size[0] - self.gm.opponent_size[1])/2
        self.gm.opponent_xoffset = self.gm.size[0]


        #========================
        # if we are using an olpc
        if olpcgames.ACTIVITY:
            self.gm.size = olpcgames.ACTIVITY.game_size

        self.gm.background = my_load_image('spacebg.jpg')
        
    
        #============================
        # Select the proper charecter
        if self.charecterselection is 'python':
            self.gm.player_cannon_offset = (-20, 45)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = FlyingSaucer(self.gm)
        elif self.charecterselection is 'tux':
            self.gm.player_cannon_offset = ( 90, 30)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = SpaceShuttle(self.gm)
        elif self.charecterselection is 'gnu':
            self.gm.player_cannon_offset = ( 100, 0)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = ClassicRocket(self.gm)
        elif self.charecterselection is 'wilber':
            self.gm.player_cannon_offset = (10, 20)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = FighterJet(self.gm)
        else:
            self.gm.player_cannon_offset = (-20, -150)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = FlyingSaucer(self.gm)

        #=======================
        # Setup all the managers
        self.gm.opponent_manager = TheOpponent(self.gm)
        self.gm.lifemanager = LifeManager(self.gm)
        self.gm.messages = ExclaimMessage(self.gm)
        self.gm.straybullets = StrayBulletManager(self.gm)

        self.gm.play = True
        self.gm.menu = False

        self.gm.player_speed = config.playerspeed
        self.gm.setup_hooks()
        
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Hook for ending the game
        @self.gm.p.subscribe(event='end_game', needs=['clean'])
        def example_hook(p, clean):
            if clean:
                self.gm.gp.mark_played(self.levelid)
                self.newstate = self.gm.gp.get_next_level(self.gm.level)
                return
            else:
                self.pop_state()
                return
        #
        #--------------------------------------------------------------


        self.screen_state.set_background(self.gm.background)
        self.gm.player_group.add(self.gm.player)
        self.gm.player_group.add(self.gm.player_cannon)
        self.t = 0
        self.useonce = True

    def main_loop(self):
        
        events = pygame.event.get( )
        
        #==========================================================
        # Main Event Loop
        if events:
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit = True
                    self.pop_state()

                elif event.type == pygame.KEYDOWN:
                    if keys(event, 'escape'):
                        self.quit = True
                        self.pop_state()
                    if keys(event, 'left'):
                        self.gm.p.trigger(event='key_left_press')
                    if keys(event, 'right'):
                        self.gm.p.trigger(event='key_right_press')
                    if keys(event, 'up'):
                        self.gm.p.trigger(event='key_up_press')
                    if keys(event, 'down'):
                        self.gm.p.trigger(event='key_down_press')
                    if keys(event, 'next'):
                        self.gm.p.trigger(event='button_next_press')
                    if keys(event, 'back'):
                        self.gm.p.trigger(event='button_back_press')


                elif event.type == pygame.KEYUP:
                    if keys(event, 'left'):
                        self.gm.p.trigger(event='key_left_rel')
                    if keys(event, 'right'):
                        self.gm.p.trigger(event='key_right_rel')
                    if keys(event, 'up'):
                        self.gm.p.trigger(event='key_up_rel')
                    if keys(event, 'down'):
                        self.gm.p.trigger(event='key_down_rel')
        #
        #------------------------------------------------------------
        
        #=====================
        # Update Sprite Groups
        self.gm.player_group.update()
        self.gm.friendly_bullet_group.update()
        self.gm.opponent_bullet_group.update()
        self.gm.opponent_group.update()
        self.gm.straybullets.update()
        self.gm.opponent_manager.update()
        self.gm.lifemanager.update()
        self.gm.messages_group.update()
        
        #==========================
        # Draw groups to the screen
        self.gm.player_group.draw()
        self.gm.friendly_bullet_group.draw()
        self.gm.opponent_group.draw()
        self.gm.opponent_bullet_group.draw()
        self.gm.question_group.draw()
        self.gm.life_group.draw()
        self.gm.messages_group.draw()

        #================
        # Draw the screen
        GetScreen().draw()
