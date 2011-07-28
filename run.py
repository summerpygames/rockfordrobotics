#!/usr/bin/env python
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

# Make a new global GameManager, persistant through levels
globalgm = GameManager()

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
        """Change the speed of the text
        
        Arguments:
        x -- movement to the left
        y -- movement to the top
        """
        self.change_x+=x
        self.change_y+=y
        
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

class Enemy(MovingSvgObject):
    
    """Enemy is the basic non-friendly thing in the game
    
    An Enemy is something in general that you want to shoow, although if it is a
    wrong answer it is something that you do not want to shoot, but in any case
    still some remain that you do want to shoot
    
    """
    
    def __init__(self, size, svg, position, speed = -1, copy = False):
        self.pos = position
        self.siz = size
        super(Enemy, self).__init__(position = self.pos, svg = svg, size =
                                    self.siz, copy = copy)
        self.change_x = speed

    def update(self):
        """This just passes the update up the line"""
        super(Enemy, self).update()

class AnswerPrinter(Sprite):

    """Prints a math answer in different ways depending on what it is
    
    If the answer has a fraction in it, this will take that into account, if the
    answer is a devision with a remainder, this will take that into accound too.
    
    """

    def __init__(self):
        super(AnswerPrinter, self).__init__()
        
    
class AnswerGuy(MaskSprite):
    
    """Answer guy extends Enemy, you can shoot it to solve a problem
    
    the correct argument is important because it allows the answerguy to know
    what it should do to you when it is hit, also you need to pass it something
    to write on itself
    
    """
    
    def __init__(self, position, size, friendly_bulletgroup, friendly_player,
                 correct,  gm, response, copy =  False):
        self.pos = position
        self.siz = size
        self.friendly_bulletgroup = friendly_bulletgroup
        self.gm = gm
        self.correct = correct
                
        if copy is not False and copy.__class__ == svgsprite.SVGSprite:
            self.svg = copy.copy()
        else:
            self.data = open(os.path.join("data", "numenemy.svg")).read()
            self.svg = svgsprite.SVGSprite(svg = self.data,
                                           size = self.siz)

        self.text = response
        super(AnswerGuy, self).__init__()
        self.change_x = -1
        self.change_y = 0
        self.image = new_surface(size)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.position = (self.pos[0], self.pos[1])
        self.image.blit(self.svg.image, (0, 0))
        self.image.blit(self.text.image, (self.siz[0] / 3, self.siz[1] / 3))
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.friendly_player = friendly_player

    def update(self):
        """This will update the Answers, change their direction, stuff like
        that, it will also see if they have been hit, in that case if it is a
        correct answer will call for you to go on to the next level, and in the
        case that it is an incorrect answer will do that plus show the correct
        answer on the screen then subtract a life.
        """
        collisions = pygame.sprite.spritecollide(self,
                                                 self.friendly_bulletgroup,
                                                 True,
                                                 pygame.sprite.collide_mask)
        if len(collisions) > 0:
            self.gm.p.trigger(event='shot_answer', correct=self.correct)
            self.kill()
        self.rect.top += self.change_y
        self.rect.left += self.change_x

        super(AnswerGuy, self).update()

class BadGuy(Enemy):

    """A BadGuy is a simple enemy, it only can be destroyed or destroy you.

    The BadGuy will shoot you when you are in its path, but will only shoot
    again once you have cleared and reentered its path, so stay out of its way!
    
    """
    def __init__(self, position, size, friendly_bulletgroup,
                 opponent_bulletgroup, bullets, friendly_player, gm, copy = False):
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
        collisions = pygame.sprite.spritecollide(self,
                                                 self.friendly_bulletgroup,
                                                 True,
                                                 pygame.sprite.collide_mask)
        if len(collisions) > 0:
            self.kill()
            self.gm.p.trigger(event='strays', bulletlist = self.bullets,
                            bulletgroup = self.opponent_bulletgroup)

        super(BadGuy, self).update()
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

        for i in self.bullets:
            if i.rect.left < -20:
                i.remove(self.opponent_bulletgroup)
                self.bullets.remove(i)


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
        self.sounds.append(pygame.mixer.Sound(os.path.join('data',
                                                           'highlaser.wav')))
        self.sounds.append(pygame.mixer.Sound(os.path.join('data',
                                                           'midlaser.wav')))
        self.sounds.append(pygame.mixer.Sound(os.path.join('data',
                                                           'lowlaser.wav')))
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
        else:
            print 'HOT'

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
        if self.heat > 0:
            self.heat -= 1
        elif self.overheated == True:
            self.overheated = False
            print 'COOL'
        if self.overheated:
            self.redness.fill((255, 0, 0))
        else:
            self.redness.fill(self.color_finder(self.heat))
        self.image.blit(self.redness, (0, 0, self.heat, 15))
        self.image.blit(self.blackness, (self.heat, 0, 75 -
                                         self.heat, 0)) 
        for i in self.bullets:
            if i.rect.left > self.gm.size[0]:
                i.remove(self.bulletgroup)
                self.bullets.remove(i)

        super(LaserCannon, self).update()

class StrayBulletManager(object):
    """Cleans up stray bullets left behind by enemies that have died
    
    A pangler trigger is used to signal this class that it should be monitoring
    stray bullets for a perticular bullet list. Pass a list of bullets along
    with the panglery trigger and let the stray bullet manager update and
    monitor the positions of the lost bullets. after a list of bullets is fully
    depleted, the list will be removed from the que
    
    """

    def __init__(self, gm):
        self.straylists = []
        self.gm = gm
        @self.gm.p.subscribe(event='strays', needs=['bulletlist', 'bulletgroup'])
        def strays_hook(p, bulletlist, bulletgroup):
             self.straylists.append([bulletlist, bulletgroup])

    def update(self):
        """Update the lists of stray bullets"""
        for i in self.straylists:
            for g in i[0]:
                if g.rect.left < -25:
                    g.remove(i[1])
                    i[0].remove(g)




class Player(MovingSvgObject):
    
    """Player is the generic player, it should be extended by a type of player
    
    The player will respond when it is hit by an enemy bullet, or an enemy, but
    that is about it besides doing what all other Moving SVG objects do
    
    """
    
    def __init__(self, svg, lasercannon):
        super(Player, self).__init__(position = (10, 10), svg = svg, size =
                                     (200, None))
        self.cannon = lasercannon

    def shoot(self, position):
        """This will make the plater shoot"""
        self.cannon.shoot(position)

    def update(self):
        """This is an extention of the update that is used for the movind
        object
        """
        collisions = pygame.sprite.spritecollide(self,
                                                 self.opponent_bulletgroup,
                                                 True,
                                                 pygame.sprite.collide_mask)
        if len(collisions) > 0:
            print '''FAIL!!
FAILURE!!!
LOOOOSERRR!!!
YOU STIIINNNK!!!
'''

        super(Player, self).update()

        
class FlyingSaucer(Player):
    
    """Flying saucer is the vehical of choice for your favorite python.
    
    This is an extention of the Player, overriding the SVG that is displayed

    """
    
    def __init__(self, gm):
        self.cannon = gm.player_cannon
        self.opponent_bulletgroup = gm.opponent_bullet_group
        super(FlyingSaucer, self).__init__(svg=os.path.join('data',
                                                            'pythonsaucer.svg'),
                                           lasercannon = self.cannon)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(FlyingSaucer, self).shoot(self.rect.center)

class SpaceShuttle(Player):
    
    """Flying saucer is the vehical of choice for your favorite python.
    
    This is an extention of the Player, overriding the SVG that is displayed

    """
    
    def __init__(self, gm):
        self.cannon = gm.player_cannon
        self.opponent_bulletgroup = gm.opponent_bullet_group
        super(SpaceShuttle, self).__init__(svg=os.path.join('data',
                                                            'tuxshuttle.svg'),
                                           lasercannon = self.cannon)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(SpaceShuttle, self).shoot(self.rect.center)

class ClassicRocket(Player):
    
    """Flying saucer is the vehical of choice for your favorite python.
    
    This is an extention of the Player, overriding the SVG that is displayed

    """
    
    def __init__(self, gm):
        self.cannon = gm.player_cannon
        self.opponent_bulletgroup = gm.opponent_bullet_group
        super(ClassicRocket, self).__init__(svg=os.path.join('data', 'gnurocket.svg'),
                                           lasercannon = self.cannon)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(ClassicRocket, self).shoot(self.rect.center)

class FighterJet(Player):
    
    """Flying saucer is the vehical of choice for your favorite python.
    
    This is an extention of the Player, overriding the SVG that is displayed

    """
    
    def __init__(self, gm):
        self.cannon = gm.player_cannon
        self.opponent_bulletgroup = gm.opponent_bullet_group
        super(FighterJet, self).__init__(svg=os.path.join('data', 'gimpfighter.svg'),
                                           lasercannon = self.cannon)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(Fighterjet, self).shoot(self.rect.center)


class Bullet(MaskSprite):
    
    """A generic bullet, should be extended.
    
    A bullet is a laser charge that somehow travels slower than the speed of
    light, maybe by some sort of altered field I don't know, but it only can
    move and cannot think for itself
    
    """

    def __init__(self, pos, color, size, speed):
        MaskSprite.__init__(self)
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

        if not olpcgames.ACTIVITY:
            self.mask.fill()

    def changespeed(self, x, y):
        """Change the speed of the SVG"""
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


def keys(event, action):
    """A little hack to make it easier to use the other parts of the programs, I
    think it is a little unneccecary, but it is OK, just shows how you can make
    the program take more room or something
    """
    if action == 'escape':
        if event.key == pygame.K_ESCAPE:
            return True
    if action == 'left':
        if event.key == pygame.K_KP4 or event.key == pygame.K_LEFT:
            return True
    if action == 'right':
        if event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT:
            return True
    if action == 'up':
        if event.key == pygame.K_KP8 or event.key == pygame.K_UP:
            return True
    if action == 'down':
        if event.key == pygame.K_KP2 or event.key == pygame.K_DOWN:
            return True
    if action == 'space':
        if event.key == pygame.K_KP1 or event.key == pygame.K_SPACE:
            return True


class TheOpponent():
    
    """The opponent is a controller for the things that you want to shoot.
    
    The opponent contains methods for spawning enemys at any location in
    different positions. It allows the same things to be passed to every enemy
    that is created.
    
    """
    
    def __init__(self, gm):
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


    def spawn_badguys(self, screensize, number, x_offset, y_offset):
        """I will make more enemys for you"""
        self.size, self.positions = egen(screensize, number, x_offset, y_offset)
        self.badguysvg = svgsprite.SVGSprite(open(os.path.join('data',
                                                               'enemy.svg')).read(),
                                             self.size)
        for i in range(len(self.positions)):
            self.enemies.append(BadGuy(self.positions[i], self.size,
                                      self.friendly_bullet_group,
                                      self.opponent_bullet_group,
                                      self.opponent_bullets,
                                      self.friendly_player,
                                      self.gm,
                                      copy = self.badguysvg))
            self.group.add(self.enemies[-1])

    def spawn_answerguys(self, screensize, number, x_offset, y_offset):
        """I will make more enemys for you"""
        self.size, self.positions = answergen(x_offset, y_offset, screensize)
        self.answerguysvg = svgsprite.SVGSprite(open(os.path.join('data',
                                                                  'numenemy.svg')).read(),
                                                self.size)
        self.question = printer.Converter(questions.getquestion.get('addition.upto10'))
        self.question.render()
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

        self.questionsprite = self.question.getquestion()
        self.questionsprite.add(self.question_group)
        

    def update(self):
        """This will update the positions of the bullets"""
        self.opponent_bulletgroup.update()

def start_gm(gm, charecter = 1):
    """Simple code to start everything for the global game manager, it also
    sets up many of the hooks for panglery
    """

    gm.opponents = []
    gm.opponent_group = Group()
    gm.opponent_bullets = []
    gm.opponent_bullet_group =  Group()
    gm.question_group = Group()

    
    gm.player_group = Group()
    gm.playable_bullets = []
    gm.friend_bullets = []
    gm.friendly_bullet_group = Group()

    gm.size = (1200, 900)
    if olpcgames.ACTIVITY:
        gm.size = olpcgames.ACTIVITY.game_size
#    gm.screen = pygame.display.set_mode(gm.size)
    gm.background = my_load_image('deepspace.jpg')

    if charecter is 1:
        gm.player_cannon_offset = (-20, 0)
        gm.player_cannon = LaserCannon(gm)
        gm.player = FlyingSaucer(gm)
    elif charecter is 2:
        gm.player_cannon_offset = (-20, 0)
        gm.player_cannon = LaserCannon(gm)
        gm.player = FlyingSaucer(gm)
    elif charecter is 3:
        gm.player_cannon_offset = (-20, 0)
        gm.player_cannon = LaserCannon(gm)
        gm.player = FlyingSaucer(gm)
    elif charecter is 4:
        gm.player_cannon_offset = (-20, 0)
        gm.player_cannon = LaserCannon(gm)
        gm.player = FlyingSaucer(gm)
    else:
        gm.player_cannon_offset = (-20, 0)
        gm.player_cannon = LaserCannon(gm)
        gm.player = FlyingSaucer(gm)

    gm.opponent_manager = TheOpponent(gm)

    gm.playerlifes = 3
    

    gm.straybullets = StrayBulletManager(gm)

    gm.play = True
    gm.menu = False

    gm.player_speed = 10

    gm.setup_hooks()

###############################################################################

class PlayState(SubGame):
    
    def __init__(self, charecter):
        
        SubGame.__init__(self)
        self.initialized = False
        self.charecterselection = charecter

    def transition_in(self):
        # This code is for the APH, to make sure that we do not transition 2
        # times
        if self.initialized:
            return
        self.initialized = True
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        pygame.init()
        self.gm = globalgm
        self.set_layers(['test'])
        self.gm.opponents = []
        self.gm.opponent_group = Group()
        self.gm.opponent_bullets = []
        self.gm.opponent_bullet_group =  Group()
        self.gm.question_group = Group()

        
        self.gm.player_group = Group()
        self.gm.playable_bullets = []
        self.gm.friend_bullets = []
        self.gm.friendly_bullet_group = Group()

        self.gm.size = (800, 600)
        if olpcgames.ACTIVITY:
            self.gm.size = olpcgames.ACTIVITY.game_size
    #    self.gm.screen = pygame.display.set_mode(self.gm.size)
        self.gm.background = my_load_image('spacebg.jpg')
        print self.charecterselection
        if self.charecterselection is 'python':
            self.gm.player_cannon_offset = (-20, 0)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = FlyingSaucer(self.gm)
        elif self.charecterselection is 'tux':
            self.gm.player_cannon_offset = (-20, 0)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = SpaceShuttle(self.gm)
        elif self.charecterselection is 'gnu':
            self.gm.player_cannon_offset = (-20, 0)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = ClassicRocket(self.gm)
        elif self.charecterselection is 'wilber':
            self.gm.player_cannon_offset = (-20, 0)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = FighterJet(self.gm)
        else:
            self.gm.player_cannon_offset = (-20, 0)
            self.gm.player_cannon = LaserCannon(self.gm)
            self.gm.player = FlyingSaucer(self.gm)

        self.gm.opponent_manager = TheOpponent(self.gm)

        self.gm.playerlifes = 3
        

        self.gm.straybullets = StrayBulletManager(self.gm)

        self.gm.play = True
        self.gm.menu = False

        self.gm.player_speed = 10

        self.gm.setup_hooks()
        self.screen_state.set_background(self.gm.background)
        self.gm.player_group.add(self.gm.player)
        self.gm.player_group.add(self.gm.player_cannon)
        self.t = 0
        
    def main_loop(self):
        
        events = pygame.event.get( )
        
        # Now the main event-processing loop
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
                    if keys(event, 'space'):
                        self.gm.p.trigger(event='key_x_press')
                        self.gm.player.shoot()
                    if event.key == pygame.K_KP3 or event.key == pygame.K_s:
                        self.gm.opponent_manager.spawn_badguys((600, 600), 9,
                                                               700,
                                                          50)
                    if event.key == pygame.K_KP9 or event.key == pygame.K_a:
                        self.gm.opponent_manager.spawn_answerguys((600, 600), 9,
                                                                  700,
                                                          50)


                elif event.type == pygame.KEYUP:
                    if keys(event, 'left'):
                        self.gm.p.trigger(event='key_left_rel')
                    if keys(event, 'right'):
                        self.gm.p.trigger(event='key_right_rel')
                    if keys(event, 'up'):
                        self.gm.p.trigger(event='key_up_rel')
                    if keys(event, 'down'):
                        self.gm.p.trigger(event='key_down_rel')
            
        
        #Update various sprite groups
        self.gm.player_group.update()
        self.gm.friendly_bullet_group.update()
        self.gm.opponent_bullet_group.update()
        self.gm.opponent_group.update()
        self.gm.straybullets.update()

        self.gm.player_group.draw()
        self.gm.friendly_bullet_group.draw()
        self.gm.opponent_group.draw()
        self.gm.opponent_bullet_group.draw()
        self.gm.question_group.draw()
        GetScreen().draw()
        
        

if __name__ == '__main__':
    main()
