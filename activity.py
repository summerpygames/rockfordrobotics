from olpcgames import activity
from gettext import gettext as _

class Activity(activity.PyGameActivity):
    """Sugar activity launcher script"""
    
    game_name = 'launcher'
    game_title = _('Laser Math Game')
    game_size = None
