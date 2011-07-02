import olpcgames, pygame, logging 
from olpcgames import pausescreen, textsprite, svgsprite
from egen import egen as egen
from random import *
import os
import panglery
log = logging.getLogger( 'HelloPygame run' )
log.setLevel( logging.DEBUG )


class GameManager(object):
    """GameManager keeps all the values for everything the user or developer
    will encounter in the game.
    
    This can be used to store all lists and things that will need to be accessed
    at a later time, or anything that needs to be references to in many objects"""
    def __init__(self, init=1):
        self.init = init
        self.p = panglery.Pangler()
        
# -- Attributes
# Set speed vector
class MovingTextObject(textsprite.TextSprite):
    """docstring for somehting"""
    def __init__(self, text=None, family=None, size=None, bold=False,
                 italic=False, color=None, background=None):

        super(MovingTextObject, self).__init__(text, family, size,
                                        bold, italic, color,
                                        background)
        self.change_y = 0
        self.change_x = 0


            
    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x+=x
        self.change_y+=y
        
    # Find a new position for the player
    def update(self):
        self.rect.top += self.change_y
        self.rect.left += self.change_x

class MovingSvgObject(svgsprite.SVGSprite):
    """This is a moving svg object, you can make it do all sorts of stuff."""
    def __init__(self, position = (0, 0), svg=None, size=None):
        data = open(svg).read()
        super(MovingSvgObject, self).__init__(data, size)
        self.rect.top = position[1]
        self.rect.left = position[0]
        self.change_x = 0
        self.change_y = 0

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x+=x
        self.change_y+=y
        
    # Find a new position for the player
    def update(self):
        self.rect.top += self.change_y
        self.rect.left += self.change_x

class Enemy(MovingSvgObject):
    """This is a nonfriendly moving object this will be booth a question and a
    bad guy"""
    def __init__(self, size, svg, position, speed = -1):
        self.position = position
        self.size = size
        super(Enemy, self).__init__(position = self.position, svg = svg, size =
                                    self.size)
        self.change_x = speed
    def update(self):
        """This just passed the update up the line"""
        super(Enemy, self).update()
    
class BadGuy(Enemy):
    """You can shoot all bad guys, unlike incorrect enemys"""
    def __init__(self, position, size, friendly_bulletgroup,
                 opponent_bulletgroup, bullets, friendly_player):
        self.position = position
        self.size = size
        self.friendly_bulletgroup = friendly_bulletgroup
        self.opponent_bulletgroup = opponent_bulletgroup
        self.bullets = bullets
        super(BadGuy, self).__init__(position = self.position, size = self.size,
                                     svg = os.path.join('data', 'enemy.svg'))
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.friendly_player = friendly_player
        self.onefire = False
        self.bullet_offset = (0, 0)
    def update(self):
        """This will update the bad guy and make sure it is not touching any
        bullets or the other wall."""
        collisions = pygame.sprite.spritecollide(self,
                                                 self.friendly_bulletgroup,
                                                 True,
                                                 pygame.sprite.collide_mask)
        if len(collisions) > 0:
            self.kill()

        super(BadGuy, self).update()
        if ((self.rect.midleft[1] >= self.friendly_player.rect.topright[1])
        and (self.rect.midleft[1] <= self.friendly_player.rect.bottomright[1])):
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

class LaserCannon(pygame.sprite.Sprite):

    # -- Attributes
    # Set speed vector
    change_x=0
    change_y=0
    
    # -- Methods
    # Constructor function
    def __init__(self, gm):
        # Call the parent's constructor
        self.gm = gm
        pygame.sprite.Sprite.__init__(self)
        self.sounds = []
        self.offset = gm.player_cannon_offset
        self.sounds.append(pygame.mixer.Sound(os.path.join('data',
                                                           'highlaser.wav')))
        self.sounds.append(pygame.mixer.Sound(os.path.join('data',
                                                           'midlaser.wav')))
        self.sounds.append(pygame.mixer.Sound(os.path.join('data',
                                                           'lowlaser.wav')))
        self.bulletgroup = gm.friendly_bullet_group
        # Set height, width
        self.blackness = pygame.Surface([75, 15])
        self.blackness.fill((0, 0, 0))
        self.redness = pygame.Surface([75, 15])
        self.image = pygame.Surface([75, 15])
        self.redness.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

       
        # Make our top-left corner the passed-in location.
        
        self.overheated = False
        self.heat = 0

        self.bullets = gm.playable_bullets
    def overheat(self):
        """This will make the cannon overheated"""
        self.overheated = True
        self.heat = 75
    def shoot(self, position):
        if self.overheated == False:
            """This is called for the cannon object to shoot something"""
            self.bullets.append(FriendlyBullet((position[0] + self.offset[0],
                                               position[1] + self.offset[1])))
            self.heat += 20
            self.bulletgroup.add(self.bullets[-1])
            choice(self.sounds).play()
            if self.heat >= 75:
                self.overheat()
        else:
            print 'HOT'

    def color_finder(self, heat):
        """This will chose a color based on how hot the gun is"""
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
            i.update()
            if i.rect.left > 800:
                i.remove(self.bulletgroup)
                self.bullets.remove(i)

class Player(MovingSvgObject):
    """This is the good guy, the one that can shoot the lasers and kill the bad
    guys and get the math problems"""
    def __init__(self, svg, lasercannon):
        super(Player, self).__init__(position = (10, 10), svg = svg, size =
                                     (150, 150))
        self.cannon = lasercannon
    def shoot(self, position):
        """This will make the plater shoot"""
        self.cannon.shoot(position)

    def update(self):
        """This is an extention of the update that is used for the movind object"""
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
    """This is just the class for the flying saucer or the ufo"""
    def __init__(self, gm):
        self.cannon = gm.player_cannon
        self.opponent_bulletgroup = gm.opponent_bullet_group
        super(FlyingSaucer, self).__init__(svg=os.path.join('data', 'ufo.svg'),
                                           lasercannon = self.cannon)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(FlyingSaucer, self).shoot(self.rect.center)

class Bullet(MovingSvgObject):
    def __init__(self, pos, svg, size, speed):
        super(Bullet, self).__init__(pos, svg, size)
        self.change_x = speed
 
class FriendlyBullet(Bullet):
    def __init__(self, pos, svg = os.path.join('data', 'lit_laser_green.svg'),
                 size = (50, 50), speed=30):
        super(FriendlyBullet, self).__init__(pos, svg, size, speed)

class BadBullet(Bullet):
    def __init__(self, pos, svg = os.path.join('data', 'friendly_laser.svg'),
                 size = (50, 50), speed=-15):
        super(BadBullet, self).__init__(pos, svg, size, speed)

    
def keys(event, action):
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
    """Contains things about the enemy you only wished you knew"""
    def __init__(self, gm):
        self.gm = gm
        self.enemies = gm.opponents
        self.group = gm.opponent_group
        self.opponent_bullets = gm.opponent_bullets
        self.friendly_bullet_group = gm.friendly_bullet_group
        self.opponent_bullet_group = gm.opponent_bullet_group
        self.friendly_player = gm.player

    def spawn_badguys(self, screensize, number, x_offset, y_offset):
        """I will make more enemys for you"""
        self.size, self.positions = egen(screensize, number, x_offset, y_offset)
        for i in range(len(self.positions)):
            self.enemies.append(BadGuy(self.positions[i], self.size,
                                      self.friendly_bullet_group,
                                      self.opponent_bullet_group,
                                      self.opponent_bullets,
                                      self.friendly_player))
            self.group.add(self.enemies[-1])

    def update(self):
        """This will update the positions of the bullets"""
        self.opponent_bulletgroup.update()

def start_gm(gm, charecter = 1):

    gm.opponents = []
    gm.opponent_group = pygame.sprite.OrderedUpdates()
    gm.opponent_bullets = []
    gm.opponent_bullet_group =  pygame.sprite.OrderedUpdates()
    
    gm.player_group = pygame.sprite.OrderedUpdates()
    gm.playable_bullets = []
    gm.friend_bullets = []
    gm.friendly_bullet_group = pygame.sprite.OrderedUpdates()
    
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

def main():
    """The mainlook which is specified in the activity.py file
    
    "main" is the assumed function name"""
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
    clock = pygame.time.Clock()
    sp = 10 # The speed of the player
    
    
    size = (800,600)
    if olpcgames.ACTIVITY:
        size = olpcgames.ACTIVITY.game_size
    screen = pygame.display.set_mode(size)
    background = pygame.image.load(os.path.join('data', 'spacesmall.png'))
    # Create an 800x600 sized screen
    gm = GameManager()

    start_gm(gm)

        
    gm.player_group.add(gm.player)
    gm.player_group.add(gm.player_cannon)
    

    running = True
    while running:
        screen.blit(background, (0, 0))
#        milliseconds = clock.tick(100) # maximum number of frames per second
        #MESS WITH THIS^^^^^^^^^^^^^^^
        # Event-management loop with support for pausing after X seconds (20 here)
        events = pausescreen.get_events()
        clock.tick(25)
        # Now the main event-processing loop
        if events:
            for event in events:
                log.debug( "Event: %s", event )
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if keys(event, 'escape'):
                        running = False
                    if keys(event, 'left'):
                        gm.player.changespeed(-sp,0)
                    if keys(event, 'right'):
                        gm.player.changespeed(sp,0)
                    if keys(event, 'up'):
                        gm.player.changespeed(0,-sp)
                    if keys(event, 'down'):
                        gm.player.changespeed(0,sp)
                    if keys(event, 'space'):
                        gm.player.shoot()
                    if event.key == pygame.K_KP3 or event.key == pygame.K_s:
                        gm.opponent_manager.spawn_badguys((400, 400), 9, 800, 100)

                elif event.type == pygame.KEYUP:
                    if keys(event, 'left'):
                        gm.player.changespeed(sp,0)
                    if keys(event, 'right'):
                        gm.player.changespeed(-sp,0)
                    if keys(event, 'up'):
                        gm.player.changespeed(0,sp)
                    if keys(event, 'down'):
                        gm.player.changespeed(0,-sp)
        gm.player_group.update()
        gm.friendly_bullet_group.draw(screen)
        gm.player_group.draw( screen )
        gm.opponent_group.update()
        gm.opponent_group.draw(screen)
        gm.opponent_bullet_group.update()
        gm.opponent_bullet_group.draw(screen)
        pygame.display.flip()
#        clock.tick(500)

    pygame.quit()

if __name__ == '__main__':
    main()
