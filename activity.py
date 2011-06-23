from olpcgames import activity
from gettext import gettext as _

class Activity(activity.PyGameActivity):
    """Your Sugar activity"""
    
    game_name = '%(mainloop)s'
    game_title = _('%(title)s')
    game_size = None
