import pygame
from APH import *
from APH.Game import *
from APH.Screen import *

class BackgroundExample(NewGame):
    def transition_in(self):
        screen = self.screen_state
        screen.set_background(load_image("assets/big_stars.jpg"))
        
    def main_loop(self):
        GetScreen().draw()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.quit = True
        
if __name__ == "__main__":
    g = BackgroundExample((255, 255, 255), (640, 480), (640, 480), False)
    g.push_state()
    clock = pygame.time.Clock()

    while not GetGame().quit:
        clock.tick(30)
        GetGame().main_loop()