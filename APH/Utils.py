import pygame
from pygame.locals import *

class memoize(object):
    """ This is a decorator to allow memoization of function calls. It clears
    the cache only on state changes. """
    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.state = None
    def __call__(self, *args):
        from Game import GetGame
        if GetGame() is not self.state:
            self.state = GetGame()
            self.cache = {}
        try:
            return self.cache[args]
        except KeyError:
            res = self.func(*args)
            self.cache[args] = res
            return res
        except TypeError:
            print "WARNING: Unhashable type passed to memoize. Reconsider using this decorator"
            return self.func(*args)
    def __repr__(self):
        return self.func.__doc__

class memoize2(object):
    """ This is a decorator to allow memoization of function calls. Its cache
    is cleared on state changes, and also clears items from the cache which
    haven't been used in at least 250 frames. """
    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.state = None
        self.last_clear = 0
    def __call__(self, *args):
        from Game import GetGame
        frame = GetGame().frame
        if GetGame() is not self.state:
            self.state = GetGame()
            self.cache = {}
        if frame - self.last_clear > 100:
            for key, value in self.cache.items():
                data, oldframe = value
                if frame - oldframe > 250:
                    self.cache.pop(key)
            self.last_clear = frame
        try:
            data, oldframe = self.cache[args]
            self.cache[args] = (data, frame)
            return data
        except KeyError:
            res = self.func(*args)
            self.cache[args] = (res, frame)
            return res
        except TypeError:
            print "WARNING: Unhashable type passed to memoize2. Reconsider using this decorator"
            return self.func(*args)
    def __repr__(self):
        return self.func.__doc__

@memoize
def load_image(fullname, colorkey=None):
    """ Load an image from a filename. colorkey is an optional parameter, if it
    is set, then the colorkey of the image is set. If colorkey is -1, then the
    colorkey is automatically determined from the top left corner. """
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", fullname
        raise SystemExit, message
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image.convert_alpha()
    
def dist2(pt1,pt2):
    """ Returns the square of a distance between two points"""
    return (pt1[0]-pt2[0]) ** 2 + (pt1[1]-pt2[1]) ** 2
    
def smooth_rotate(surf, angle, scale=10):
    """ Performs a smoother rotation of a surface by scaling, rotating, and
    rescaling on rotations. """
    s = max(surf.get_width(), surf.get_height())
    surf2 = pygame.transform.rotozoom(surf, angle, scale)
    d = int(round((surf2.get_width() - s * scale) / 2.))
    surf2 = pygame.transform.chop(surf2, (0, 0, d, d))
    surf2 = pygame.transform.chop(surf2, (s * scale, s * scale, 2*d, 2*d))
    surf2 = pygame.transform.scale(surf2, (s, s))
    return surf2
    
def smooth_rotate_set(surf, nangles = 36, scale = 10):
    return [pygame.transform.rotate(surf, theta * 360. / nangles) for theta in range(nangles)]
    
def new_surface(size):
    """ returns a Surface guaranteed to work with APH, which has an alpha
    channel and a 32-bit color depth """
    return pygame.Surface((int(size[0]), int(size[1])), SRCALPHA, 32)