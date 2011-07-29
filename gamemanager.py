#!/usr/bin/python
'''
File: gamemanager.py
Author: Mark Amber
Description: This controls all sorts of things
'''
import panglery

class GameManager(object):

    """GameManager keeps values for everything in the game.
    
    This can be used to store all lists and things that will need to be accessed
    at a later time, or anything that needs to be references to in many
    objects
    
    """
    
    def __init__(self, init=1):
        self.init = init
        self.p = panglery.Pangler()
        
    def setup_hooks(self):
        """Setup all the hooks to use for panglery"""
        pass
        @self.p.subscribe(event='shot_answer', needs=['correct'])
        def example_hook(p, correct):
            if correct:
                print 'Yay'
            else:
                print 'Wrong'

        @self.p.subscribe(event='key_down_press')
        def key_down_press_hook(p):
            if self.play:
                self.p.trigger(event='player_speed_change', more=True, dir='down')
            
        @self.p.subscribe(event='key_up_press')
        def key_up_press_hook(p):
            if self.play:
                self.p.trigger(event='player_speed_change', more=True, dir='up')

        @self.p.subscribe(event='key_right_press')
        def key_right_press_hook(p):
            if self.play:
                self.p.trigger(event='player_speed_change', more=True,
                               dir='right')

        @self.p.subscribe(event='key_left_press')
        def key_left_press_hook(p):
            if self.play:
                self.p.trigger(event='player_speed_change', more=True, dir='left')

        @self.p.subscribe(event='key_down_rel')
        def key_down_rel_hook(p):
            if self.play:
                self.p.trigger(event='player_speed_change', more=False, dir='down')
  
        @self.p.subscribe(event='key_up_rel')
        def key_up_rel_hook(p):
            if self.play:
                self.p.trigger(event='player_speed_change', more=False, dir='up')
    
        @self.p.subscribe(event='key_right_rel')
        def key_right_rel_hook(p):
            if self.play:
                self.p.trigger(event='player_speed_change', more=False,
                               dir='right')
    
        @self.p.subscribe(event='key_left_rel')
        def key_left_rel_hook(p):
            if self.play:
                self.p.trigger(event='player_speed_change', more=False, dir='left')
    
        @self.p.subscribe(event='button_back_press') # 1
        def button_check_press_hook(p):
            self.p.trigger(event='end_game', clean=False)

        @self.p.subscribe(event='button_next_press') # 3
        def button_x_press_hook(p):
            self.player.shoot()



        ###############################################################
        # Start New level                                             #
        ###############################################################
        @self.p.subscribe(event='spawn_wave')
        def example_hook(p):
            try:
                if self.gameplaylist.pop(-1) == 'A':
                    self.opponent_manager.spawn_answerguys()
                else:
                    self.opponent_manager.spawn_badguys(int(self.gameplaylist.pop(-1)))
            except IndexError:
                self.p.trigger(event='end_game', clean=True)

                

        

        @self.p.subscribe(event='player_speed_change', needs=['more', 'dir'])
        def player_speed_change_hook(p, more, dir):
            """This is a hook for the speed change of the player
            
            arguments:
            more -- If this is true that is faster, false then slower
            dir  -- The direction, up down left or right
            """
            if more:
                sp = self.player_speed
            else:
                sp = -self.player_speed
            if dir == 'up':
                arg = (0, -sp)
            elif dir == 'down':
                arg = (0, sp)
            elif dir == 'left':
                arg = (-sp, 0)
            elif dir == 'right':
                arg = (sp, 0)
            else:
                arg = (0, 0)

            self.player.changespeed(*arg)

