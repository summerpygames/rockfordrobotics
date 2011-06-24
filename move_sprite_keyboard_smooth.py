# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu

import olpcgames, pygame, logging 
from olpcgames import pausescreen, textsprite, svgsprite
from gettext import gettext as _
import resources as r
log = logging.getLogger( 'HelloPygame run' )
log.setLevel( logging.DEBUG )


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
    def __init__(self, position = (0,0), svg=None, size=None):
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

class Player(MovingSvgObject):
    """This is the good guy, the one that can shoot the lasers and kill the bad
    guys and get the math problems"""
    def __init__(self, svg, bullets):
        super(Player, self).__init__(position = (10, 10), svg = svg, size =
                                     (100, 100))
        self.bullets = bullets
        
    def shoot(self, position):
        """This is called for the moving player object to shoot something"""
        self.bullets.append(Bullet(position))

class FlyingSaucer(Player):
    """This is just the class for the flying saucer or the ufo"""
    def __init__(self, bullets):
        super(FlyingSaucer, self).__init__(svg='ufo.svg', bullets = bullets)
    def shoot(self):
        """This is what you run when you want the thing to fire a laser"""
        super(FlyingSaucer, self).shoot(self.rect.center)
        

class Bullet(MovingSvgObject):
    def __init__(self, pos, svg = 'laser.svg', size = (25, 25), speed=30):
        super(Bullet, self).__init__(pos, svg, size)
        self.change_x = speed
    
        

def main():
    """The mainlook which is specified in the activity.py file
    
    "main" is the assumed function name"""
    bullets = []
    
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

    player = FlyingSaucer(bullets)
    group = pygame.sprite.RenderUpdates()
    
    group.add( player )
    
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill( (0,0,128))
        milliseconds = clock.tick(25) # maximum number of frames per second
        
        # Event-management loop with support for pausing after X seconds (20 here)
        events = pausescreen.get_events()
        # Now the main event-processing loop
        if events:
            for event in events:
                log.debug( "Event: %s", event )

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_KP4 or event.key == pygame.K_LEFT:
                        player.changespeed(-1,0)
                    if event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT:
                        player.changespeed(1,0)
                    if event.key == pygame.K_KP8 or event.key == pygame.K_UP:
                        player.changespeed(0,-1)
                    if event.key == pygame.K_KP2 or event.key == pygame.K_DOWN:
                        player.changespeed(0,1)
                    if event.key == pygame.K_KP1 or event.key == pygame.K_SPACE:
                        player.shoot()


                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_KP4 or event.key == pygame.K_LEFT:
                        player.changespeed(1,0)
                    if event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT:
                        player.changespeed(-1,0)
                    if event.key == pygame.K_KP8 or event.key == pygame.K_UP:
                        player.changespeed(0,1)
                    if event.key == pygame.K_KP2 or event.key == pygame.K_DOWN:
                        player.changespeed(0,-1)
        for j in bullets:
            j.update()
            if j.rect.left > 800:
                j.remove(group)
                bullets.remove(j)
        
        for j in bullets:
                j.add(group)
        player.update()
        group.draw( screen )
        pygame.display.flip()
        clock.tick(500)

    pygame.quit()

if __name__ == '__main__':
    main()
