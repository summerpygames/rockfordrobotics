import pygame
from Utils import memoize
from math import floor, ceil
from Screen import ScreenState

# These two funcs need to be here due to cyclic dependencies if put elsewhere.
def GetGame():
    """ Returns the current GameState. """
    return GameState.stack[-1]
    
def GetScreen():
    """ Returns the current ScreenState from the current GameState"""
    return GetGame().screen_state

class GameState(object):
    """ Controls the current state of the program. """
    stack = []
    frame = -1
    
    def __init__(self):
        """ Do some initialization. This puts filler variables in place
        of required instance variables. """
        self.quit = False
        self.screen_state = None
        self._layers = ['none']
        self.fps = None
        self.fps_log = []
    
    def transition_in(self):
        """ Called when this state is transitioned into being. """
        pass

    def transition_out(self):
        """ Called when this state is transitioned out of being. """
        pass
        
    def main_loop(self):
        """ Called once per frame. Should be sure to draw its
        ScreenState. """
        pass
        
    def swap_state(self):
        """ Pops the current state off the stack, and then pushes the caller
        onto the stack and transitions into it."""
        if GameState.stack != []:
            g = GameState.stack.pop()
            g.transition_out()
        GameState.stack.append(self)
        GetScreen().redraw()
        ## Clear the event queue on state transitions
        pygame.event.get()
        self.transition_in()

        
    def push_state(self):
        """ Pushes the current state onto the stack and transitions into it. """
        if GameState.stack != []:
            GameState.stack[-1].transition_out()
        GameState.stack.append(self)
        GetScreen().redraw()
        ## Clear the event queue on state transitions
        pygame.event.get()
        self.transition_in()
        
    def pop_state(self):
        """ Pops the current state off of the stack and transitions back
        into the previous state. """
        self.transition_out()
        g = GameState.stack.pop()
        GetScreen().redraw()
        ## Clear the event queue on state transitions
        pygame.event.get()
        if GameState.stack != []:
            GameState.stack[-1].transition_in()
        else:
            exit()
        
    def set_layers(self, layers):
        """ Sets the layers for the current game state, as a list of layers
        from bottom-most to top-most. """
        self._layers = layers
        self.screen_state.set_layers(layers)
        
    def get_layers(self):
        return self._layers[:]
        
    def test_quit(self):
        if len(pygame.event.get(pygame.QUIT)) > 0:
            self.quit = True
            
    def main(self, clock, fps):
        """ Calls the main loop function, and runs other APH facilities which
        need to be run on a frame by frame basis. """
        GameState.frame += 1
        if self.fps is not None:
            clock.tick_busy_loop(self.fps)
        else:
            clock.tick_busy_loop(fps)
        if GameState.frame > 0 and GameState.frame % 10 == 0:
            self.fps_log.append(clock.get_fps())
        self.main_loop()
        
class NewGame(GameState):
    """ Represents a new game, and sets up the screen accordingly. """
    def __init__(self, bg, virtual_size, real_size = (0,0), fullscreen = False):
        """ See: ScreenState.__init__ """
        GameState.__init__(self)
        self.screen_state = ScreenState(bg, virtual_size, real_size, fullscreen)

class SubGame(GameState):
    """ A game state which will set up the screen with the same parameters as
    used earlier in the game. Should be the base subclass for most GameStates.
    """
    def __init__(self):
        GameState.__init__(self)
        self.screen_state = GetScreen().copy()