import pygame
from Game import *
import Mouse
from weakref import ref as wref

_all_sprites = []

def _switch_game():
    for s in _all_sprites:
        if s() is not None:
            s()._expire_static()

class Sprite(object):
    """ Analagous to Sprite in pygame, but automatically handles dirty updates,
    and supports adding self.layer to allow layered rendering. This means that
    if the Sprite is repositioned or killed, the game background will
    automatically redraw over the sprite. These sprites support one additional
    feature, setting Sprite.position will automatically set Sprite.rect to a
    rect starting from position with the size of the image, and accessing
    Sprite.position will return the top left coordinate of Sprite.rect """

    def __init__(self, *groups):
        """ Adds this sprite to any number of groups by default. """
        _all_sprites.append(wref(self))
        self._age = 0
        self._static = False
        self._image = None
        self._rect = None
        self._layer = None
        self._groups = []
        self._game = GetGame()
        self.add(*groups)
    
    def _set_static(self):
        GetScreen().static_blit(repr(self),
                                self._image,
                                self.position,
                                self._layer)
        self._static = True
    
    def _expire_static(self):
        if self._static:
            GetScreen().remove_static_blit(repr(self))
        self._static = False
        self._age = 0
        
    def _set_pos(self, pos):
        self._rect = pygame.Rect(pos, self._image.get_size())
        self._age = 0
        if self._static:
            self._expire_static()
        
    def _get_pos(self):
        return self._rect.topleft
        
    def _get_layer(self):
        if self._layer is None:
            return GetGame().get_layers()[0]
        return self._layer
        
    def _set_layer(self, layer):
        layers = GetGame().get_layers()
        if layer not in layers:
            layer = layers[0]
        self._layer = layer
        if self._static:
            self._expire_static()
        
    def _get_image(self):
        return self._image
        
    def _set_image(self, image):
        self._image = image
        if self._static:
            self._expire_static()
            
    def _get_rect(self):
        # Wish this didn't need to be done, but rects can be modified
        # indirectly by setting something like self.rect.center
        if self._static:
            self._expire_static()
        self._age = 0
        return self._rect
        
    def _set_rect(self, rect):
        if self._static:
            self._expire_static()
        self._age = 0
        self._rect = rect
        
    position = property(_get_pos, _set_pos)
    layer = property(_get_layer, _set_layer)
    image = property(_get_image, _set_image)
    rect = property(_get_rect, _set_rect)
        
    def add(self, *groups):
        self._expire_static()
        for g in groups:
            if g not in self._groups:
                self._groups.append(g)
                g.add(self)
                
    def kill(self):
        """ Remove this sprite from all groups. """
        self._expire_static()
        for g in self._groups:
            g.remove(self)
            
    def alive(self):
        """ Return True if this sprite belongs to any groups, false otherwise"""
        return len(self._groups) > 0
        
    def groups(self):
        """ Return a list of groups that this sprite belongs to. """
        return self._groups[:]
        
    def draw(self):
        """ Draw this object to the display. It will always use the current
            screen state for drawing. """
        if self._static:
            return
        if self._age > 5:
            self._set_static()
        else:
            GetScreen().moving_blit(self.image,
                                    self.position,
                                    self.layer)
            self._age += 1
                                    
    def update(self, *args):
        """ Called once per frame. """
        pass
        
    def remove(self, *groups):
        self._expire_static()
        for g in groups:
            if g in self._groups:
                self._groups.remove(g)
                
    def __del__(self):
        GetScreen().remove_static_blit(repr(self))
        
class MouseOverSprite(Sprite):
    """ Represents a set of actions which an object which needs to handle
    mouseover events should respond to. Some additional properties which
    are relevant are MouseOverSprite.hover_overlay, which should be set to True
    if the search for other items which the mouse is over should be continued
    if the mouse is over this object, or False (as it is by default) if
    the search should terminate. MouseOverSprite respects layers. """

    def __init__(self, *args):
        Sprite.__init__(self, *args)
        self.hover_overlay = False
        self.mouse_over = False

    def is_mouse_over(self, pos):
        """ Takes in a position and returns true if the mouse cursor is over
        this object. The built in method uses the sprite's rect; pixel perfect
        checks should override this method, but perhaps use rect as a first
        pass, as this method will be called every frame. """
        if self.rect.collidepoint(pos):
            return True
        return False

    def mouse_on(self):
        """ Called when the mouse moves over this sprite. """
        self.mouse_over = True

    def mouse_off(self):
        """ Called when the mouse moves off of this sprite. """
        self.mouse_over = False
        
class MouseClickSprite(Sprite):
    """ Represents a set of actions which an object needs to handle mouse
    click events should respond to. The MouseClickSprite should have a member
    variable MouseClickSprite.click_overlay, which should be set to True if
    the search for other clickable items should continue if this object is
    clicked, or False otherwise (default). MouseClickSprite respects layers. """
    
    def __init__(self, *args):
        Sprite.__init__(self, *args)
        self.click_overlay = False
        
    def is_clicked(self, event):
        """ Takes a pygame event and returns true if the mouse cursor is
        where this object should be considered clicked. The built in method uses
        the sprite's rect; pixel perfect checks should override this method, but
        perhaps use rect as a first pass, as this method will be called every
        frame. The built in method also only responds to left mouse click
        events, and only on button down """
        if event.button != 1:
            return False
        if event.type != pygame.MOUSEBUTTONDOWN:
            return False
        if self.rect.collidepoint(event.pos):
            return True
        return False
        
    def clicked(self, event):
        """ Called when this object is clicked. """
        pass
        

### Group classes ###
        
class Group(object):
    """ Behaves like sprite.Group in pygame. """
    
    def __init__(self, *sprites):
        self._sprites = list(sprites)
        
    def draw(self):
        """ Calls draw on all of its Sprites. """
        [x.draw() for x in self._sprites]
    
    def update(self, *args):
        """ Calls update on all of its Sprites. """ 
        [x.update(*args) for x in self._sprites]
        
    def remove(self, *sprites):
        """ Removes Sprites from this Group. """
        for sprite in sprites:
            if sprite in self._sprites:
                self._sprites.remove(sprite)
                sprite.remove(self)
    
    def add(self, *sprites):
        """ Adds an object to its drawable list. """
        for sprite in sprites:
            if sprite not in self._sprites:
                self._sprites.append(sprite)
                sprite.add(self)
    
    def has(self, *sprites):
        """ Return true if all sprites are contained in the group. Unlike
        pygame, this does not take an iterator for each argument, only sprites.
        """
        for sprite in sprites:
            if sprite not in self._sprites:
                return False
        return True
    
    def empty(self):
        """ Clears all sprites from the group. """
        for sprite in self._sprites:
            sprite.remove(self)
        self._sprites = []
        
    def sprites(self):
        return self._sprites[:]
        
class MouseGroup(Group):
    """ A subclass of group which is the same in every way, except on update(),
    it also handles dispatching mouse events before calling update on all of
    its Sprites. Non-MouseClickSprite and Non-MouseOverSprites may be mixed in.
    Only one MouseGroup should exist per GameState, as it will empty all mouse
    events from the queue. """
    
    def __init__(self, *args):
        Group.__init__(self, *args)
        self._mouse_previously_over = []
    
    def update(self, *args):
        layers = GetGame().get_layers()
        def sort_sprites_cmp(x, y):
            # Sorts sprites by layer from top down
            return layers.index(y.layer) - layers.index(x.layer)
        
        self._sprites.sort(sort_sprites_cmp)
        
        # Let's handle mouse clicks first
        for event in Mouse.get_events():
            if event.type == pygame.MOUSEMOTION:
                # We don't really care about these, we'll poll the
                # mouse directly later
                continue
            for sprite in self._sprites:
                if not isinstance(sprite, MouseClickSprite):
                    continue
                if sprite.is_clicked(event):
                    sprite.clicked(event)
                    if sprite.click_overlay is not True:
                        break
                        
        # Now let's handle mouseover.
        mouse_pos = Mouse.get_pos()
        mouse_now_over = []
        for sprite in self._sprites:
            if not isinstance(sprite, MouseOverSprite):
                continue
            if sprite.is_mouse_over(mouse_pos):
                mouse_now_over.append(sprite)
                # first, is this one that the mouse was previously over
                if sprite in self._mouse_previously_over:
                    if sprite.hover_overlay:
                        continue
                    else:
                        break
                # Now that we know it's not, we tell it the mouse is on it
                sprite.mouse_on()
                if sprite.hover_overlay:
                    continue
                break
        
        for sprite in self._mouse_previously_over:
            if sprite in mouse_now_over:
                continue
            sprite.mouse_off()
        
        self._mouse_previously_over = mouse_now_over
        
        Group.update(self, *args)