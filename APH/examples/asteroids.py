import pygame
import math
from APH import *
from APH.Utils import *
from APH.Game import *
from APH.Screen import *
from APH.Sprite import *

WIDTH = 1024
HEIGHT = 768
FPS = 30

SHIP_VEL_CHANGE = 1
SHIP_THETA_CHANGE = 6

class Ship(Sprite):
    def __init__(self, *groups):
        Sprite.__init__(self, *groups)
        self.orig_image = new_surface((52, 52))
        self.image = self.orig_image
        pygame.draw.aalines(self.image, (255, 255, 255), True, [(1,1), (1, 51), (51, 26)])        
        self.position = (WIDTH / 2, HEIGHT / 2)
        self.layer = 'ship'
        
        self.x_vel = 0
        self.y_vel = 0
        self.theta = 0
        self.theta_change = 0
        
        
        self.rotated = smooth_rotate_set(self.image, 72)
        
    def update(self, t):
        events = pygame.event.get(pygame.KEYDOWN)
        for event in events:
            if event.key not in [K_LEFT, K_RIGHT, K_UP]:
                pygame.event.post(event)
                continue
            if event.key == K_LEFT:
                self.theta += SHIP_THETA_CHANGE
            elif event.key == K_RIGHT:
                self.theta -= SHIP_THETA_CHANGE
            else:
                self.x_vel += SHIP_VEL_CHANGE * math.cos(self.theta * math.pi / 180)
                self.y_vel += SHIP_VEL_CHANGE * -math.sin(self.theta * math.pi / 180)
        
        self.position = (self.position[0] + self.x_vel,
                         self.position[1] + self.y_vel)
        if self.position[0] > WIDTH:
            self.position = (0, self.position[1])
        elif self.position[0] < 0:
            self.position = (WIDTH, self.position[1])
        
        if self.position[1] > HEIGHT:
            self.position = (self.position[0], 0)
        elif self.position[1] < 0:
            self.position = (self.position[0], HEIGHT)
            
        if self.theta >= 360:
            self.theta -= 360
        if self.theta < 0:
            self.theta += 360
        print self.theta
            
        # New images
        self.image = self.rotated[int(round(self.theta/5.))]
        self.rect = self.image.get_rect(center=self.rect.center)

    
class Asteroids(NewGame):
    def __init__(self, *args):
        NewGame.__init__(self, *args)
        self.set_layers(['obstacles', 'ship', 'hud'])
        self.ship = Ship()
        self.t = 0
        
        self.group = Group(self.ship)
        # Let's set key repeat
        pygame.key.set_repeat(1, 1000 / 30)
        
    def main_loop(self):
        self.t = self.t + 1
        self.group.update(self.t)
        self.group.draw()


        GetScreen().draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.quit = True
    
        
if __name__ == "__main__":
    g = Asteroids((0, 0, 0), (WIDTH, HEIGHT), (0,0), True)
    g.push_state()
    
    clock = pygame.time.Clock()

    while not GetGame().quit:
        clock.tick(FPS)
        GetGame().main_loop()
        print clock.get_fps()