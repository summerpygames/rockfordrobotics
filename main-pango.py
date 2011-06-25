# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu

import olpcgames, pygame, logging 
from olpcgames import pausescreen, svgsprite
from gettext import gettext as _
import resources as r
from egen import egen as egen
log = logging.getLogger( 'HelloPygame run' )
log.setLevel( logging.DEBUG )




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
    def __init__(self, svg, position, speed = -1):
        self.position = position
        super(Enemy, self).__init__(position = self.position, svg = svg, size =
                                    (100, 100))
        self.change_x = speed
    
class BadGuy(Enemy):
    """You can shoot all bad guys, unlike incorrect enemys"""
    def __init__(self, position):
        self.position = position
        super(BadGuy, self).__init__(position = self.position, svg =
                                     "activity.svg")
class LaserCannon(pygame.sprite.Sprite):

    # -- Attributes
    # Set speed vector
    change_x=0
    change_y=0
    
    # -- Methods
    # Constructor function
    def __init__(self, bullets):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.bulletgroup = pygame.sprite.OrderedUpdates()
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

        self.bullets = bullets
    def overheat(self):
        """This will make the cannon overheated"""
        self.overheated = True
        self.heat = 75
    def shoot(self, position):
        if self.overheated == False:
            """This is called for the cannon object to shoot something"""
            self.bullets.append(Bullet(position))
            self.heat += 20
            self.bulletgroup.add(self.bullets[-1])
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
        self.redness.fill(self.color_finder(self.heat))
        self.image.blit(self.redness, (0, 0, self.heat, 15))
        self.image.blit(self.blackness, (self.heat, 0, 75 -
                                         self.heat, 0)) 
        print self.heat
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
                                     (100, 100))
        self.cannon = lasercannon

    def shoot(self, position):
        """This will make the plater shoot"""
        self.cannon.shoot(position)

        
class FlyingSaucer(Player):
    """This is just the class for the flying saucer or the ufo"""
    def __init__(self, cannon):
        self.cannon = cannon
        super(FlyingSaucer, self).__init__(svg='ufo.svg', lasercannon = self.cannon)

    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(FlyingSaucer, self).shoot(self.rect.center)

class Bullet(MovingSvgObject):
    def __init__(self, pos, svg = 'laser.svg', size = (25, 25), speed=30):
        super(Bullet, self).__init__(pos, svg, size)
        self.change_x = speed
    
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
    def __init__(self, enemys, group):
        self.enemys = enemys
        self.group = group
        
    def spawn_badguys(self, screensize):
        """I will make more enemys for you"""
        for i in range(4):
            self.enemys.append(BadGuy(egen(screensize, i)))
            self.group.add(self.enemys[i])


def main():
    """The mainlook which is specified in the activity.py file
    
    "main" is the assumed function name"""
    bullets = []
    enemys = []
    sp = 5 # The speed of the player
    
        
    size = (800,600)
    if olpcgames.ACTIVITY:
        size = olpcgames.ACTIVITY.game_size
    screen = pygame.display.set_mode(size)
    # Create an 800x600 sized screen
    
#    text = Player(
#        text = "Hello Children of the World",
#        color = (255,255,255),
#        size = 20,
#    )
    lasercannon = LaserCannon(bullets)
    enemy = BadGuy((700, 90))
    player = FlyingSaucer(lasercannon)
    
    group = pygame.sprite.OrderedUpdates()
    group.add(player)
    group.add(lasercannon)
    opponent = TheOpponent(enemys, group)

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill( (0,0,128))
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
                        player.changespeed(-sp,0)
                    if keys(event, 'right'):
                        player.changespeed(sp,0)
                    if keys(event, 'up'):
                        player.changespeed(0,-sp)
                    if keys(event, 'down'):
                        player.changespeed(0,sp)
                    if keys(event, 'space'):
                        player.shoot()
                    if event.key == pygame.K_KP3:
                        opponent.spawn_badguys(size)

                elif event.type == pygame.KEYUP:
                    if keys(event, 'left'):
                        player.changespeed(sp,0)
                    if keys(event, 'right'):
                        player.changespeed(-sp,0)
                    if keys(event, 'up'):
                        player.changespeed(0,sp)
                    if keys(event, 'down'):
                        player.changespeed(0,-sp)
        group.update()
        lasercannon.update()
        lasercannon.bulletgroup.draw(screen)
        group.draw( screen )
        pygame.display.flip()
#        clock.tick(500)

    pygame.quit()

if __name__ == '__main__':
    main()