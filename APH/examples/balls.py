import pygame
from APH import *
import math
from APH.Utils import *
from APH.Game import *
from APH.Screen import *
from APH.Sprite import *


WIDTH = 400
HEIGHT = 300
FPS = 30.

# We'll use the Menu class to put up a silly example of a menu, just to
# demonstrate pushing and popping game states.
class Menu(NewGame):
    def __init__(self, *args):
        NewGame.__init__(self, *args)
        self.initialized = False
        # We do not do more initialization here, because often times
        # our initialization relies on getting the screen state, for instance,
        # generating new sprites. Perhaps this limitation will be alleviated
        # in future versions.
        
    def transition_in(self):
        # Initialization is pushed to here. In more complicated games,
        # you may do cleanup if in transition_out() when the state is
        # moved lower on the stack, and then have to do work when
        # the game is transitioned back in. In this case, we are only worried
        # about initializing once.
        if self.initialized:
            return
        self.initialized = True
        
        # This sets the layers for drawing, which are unique to the current
        # gamestate. 
        self.set_layers(['menu'])
        
        # This should look familiar, it is standard pygame code
        pygame.font.init()
        font = pygame.font.SysFont("", 20)
        text = font.render("Welcome to the ball demo", True, (0, 0, 0))
        
        # Here we have our first example of using Sprites. Sprites in APH
        # are almost entirely analgous to sprites in pygame. They have
        # a few required attributes. The first required one is image,
        # which should be a pygame surface that represents the sprite.
        # The second is either (a) rect or (b) position, rect being a pygame
        # rect which is located where the sprite is to be drawn, or
        # position is an (x,y) tuple where the sprite should be drawn.
        # APH transfers data from the values back and forth automatically
        # for you, you need only to set one.
        # Additionally, a layer can be added, but is optional. APH will default
        # to using the bottommost layer from the current ScreenState.
        # If a layer is set, it is rendered in the appropriate layer.
        # More features can be added to sprites by extending them, as we will
        # see later in this example
        welcome = Sprite()
        welcome.image = text
        welcome.position = ((WIDTH - text.get_width()) / 2, 100)
        
        font = pygame.font.SysFont("", 16)
        text = font.render("Press any key to continue", True, (0, 0, 0))

        cont = Sprite()
        cont.image = text
        cont.position = ((WIDTH - text.get_width()) / 2, 200)
        
        
        # Here we have a sprite group, which are again analagous to pygame's
        # groups. Here it is initialized with two sprites in the group
        self.group = Group(welcome, cont)
        
        # Here, we initialize the Circles subgame, which we will
        # push onto the stack when we need it.
        self.circles = Circles()
        
    def main_loop(self):
        # Here, we make sure that all the sprites in the group gets drawn
        self.group.draw()
        
        # We call this at the end of every frame, as it is mandatory.
        GetScreen().draw()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Transition into the Circles subgame
                self.circles.push_state()
            if event.type == pygame.QUIT:
                self.quit = True
        
# Circles is a SubGame, which is another convenience subclass of
# GameState and the one which will likely be used the most. It copies the
# information of the previous GameState's ScreenState, that is, it uses
# the same virtual resolution and real resolution parameters as were used
# previously.
class Circles(SubGame):
    def __init__(self):
        SubGame.__init__(self)
        self.initialized = False
        # The same note applies here with respect to initialization.

    def transition_in(self):
        if self.initialized:
            return
        self.initialized = True
        # Again, we set up some layers, this time three of them. The bottom
        # most layer gets listed first
        self.set_layers(['red', 'green', 'blue'])

        # Here, we make three different instances of the Ball class
        # which is a subclass of Sprite, and we'll lok at it in more detail
        # below
        red = Ball('red', (255, 0, 0), 0.25)
        green = Ball('green', (0, 255, 0), 0.125)
        blue = Ball('blue', (0, 0, 255), 0.5)

        # Here, we put all the sprites we want rendered in a group.
        self.circle_group = Group(red, green, blue)
        # Here we're going to keep a counter of the number of frames elapsed
        # As it will be used in our simulation.
        self.t = 0

    def main_loop(self):
        self.t = self.t + 1
        
        # Group.update() is a method just as in pygame which calls update()
        # on all the Sprites which are in the group. Any arguments passed to
        # Group.update() are passed along to each Sprite.update()
        self.circle_group.update(self.t)
        # Again, we draw things here
        self.circle_group.draw()
        
        # And it is mandatory that we tell APH to do all the drawing at the end
        GetScreen().draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                self.pop_state()
                

# Here we make a class that represents a ball spinning in a circle.
# It subclasses Sprite, and shows some of the more powerful things
# we can do with Sprites.
class Ball(Sprite):
    """ A silly example which has a ball revolving around a point. """
    def __init__(self, layer, color, speed, center = (200,150), arc_size = 100):
        """ Layer is the layer to render on. Color is a color tuple. Speed is
            number of revolution per second, the center is the center of the arc,
            and the arc_size is the radius of the arc. """
        # Always be sure to call the constructor of the parent when subclassing
        Sprite.__init__(self)
        
        # new_surface is an important function from APH.Utils. It creates
        # a new pygame surface suitable for drawing, but it is important to use
        # new_surface as opposed to calling pygame.surface.Surface directly,
        # as some extra details need to be added to the surface to ensure
        # proper scaled rendering, especially on the XOs.
        self.image = new_surface((22,22))
        pygame.draw.circle(self.image, color, (11, 11), 10)
        self.layer = layer
        # We give the ball a dummy position
        self.position = (0,0)

        # These are additional parameters that we have added to ball
        # in order to do the calculations we need.
        self.speed = speed
        self.arc_size = arc_size
        self.center = (200, 150)

    def update(self, t):
        # On update, we use the current frame number to compute the position
        # of the ball, and upate it, creating the spinning effect.
        # The computation here is not important, but for the curious, it is
        # just a little math. e^(i*x) = cos(x) + i*sin(x)
        # If we plot the real coordinate on one axis, and the imaginary on
        # the other, we get a unit circle. 
        theta = (float(t) / FPS) * 2 * math.pi * self.speed
        self.position = (self.center[0] + self.arc_size * math.sin(theta),
                    self.center[1] + self.arc_size * math.cos(theta))

if __name__ == "__main__":
    # This is all boilerplate from the previous example, and is what
    # __main__ is pretty much always going to look like.
    g = Menu((255, 255, 255), (WIDTH, HEIGHT), (0,0), False)
    g.push_state()
    clock = pygame.time.Clock()

    while not GetGame().quit:
        clock.tick(FPS)
        GetGame().main_loop()