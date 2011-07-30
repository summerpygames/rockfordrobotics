import pygame
from Game import GetScreen
# This will eventually implement all methods in pygame.mouse, but handling
# scaling with the current scaled resolution transparently. For now, it
# implements a subset of pygame.mouse, as well as a few extra useful functions

def get_events():
    """ Gets all the mouse related events from pygame, scaled appropriately
    to match the scaled screen resolution. """
    events = pygame.event.get([pygame.MOUSEMOTION,
                              pygame.MOUSEBUTTONUP,
                              pygame.MOUSEBUTTONDOWN])
                              
    new_events = []
    for event in events:
        # This should perhaps not use a prive method in screen, but I think
        # this belongs private still. Perhaps another class to handle
        # scaling stuff needs to be involved, but it results in a lot of
        # shared code somewhere along the line.
        new_pos = GetScreen().unscale_pos(event.pos)
        if event.type == pygame.MOUSEMOTION:
            new_rel = GetScreen().unscale_pos(event.rel)
            new_event = pygame.event.Event(pygame.MOUSEMOTION,
                                           {'pos': new_pos,
                                            'rel': new_rel,
                                            'buttons': event.buttons})
        else:
            new_event = pygame.event.Event(event.type,
                                           {'pos': new_pos,
                                            'button': event.button})
                                            
        new_events.append(new_event)
        
    return new_events

def get_pos():
    # Use pygame.event.pump() to get the most up to date mouse position
    return GetScreen().unscale_pos(pygame.mouse.get_pos())