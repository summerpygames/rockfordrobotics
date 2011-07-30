#!/usr/bin/env python
# Launcher.py
# Copyright (C) 2011 Robert Deaton and Mark Amber
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This is a simple launcher for an APH game stored in a state

import sys
import os

from APH import *
from APH.Game import *
from optparse import OptionParser
import cProfile
import time
from math import sqrt
import olpcgames

import menu


def launch():
    # Here we go for where we can put some launching code
    g = menu.MainMenu()
    g.push_state()


def main():
    resolution = (0, 0)
    fps = 30
    fullscreen = True
    virtual_size = (1200,900)
    color = (0,0,0)


    if olpcgames.ACTIVITY:
        resolution = olpcgames.ACTIVITY.game_size
        virtual_size = olpcgames.ACTIVITY.game_size
        fps = 20
        fullscreen = False
    
                
    try:
        clock = pygame.time.Clock()
        g = NewGame(color, virtual_size, resolution, fullscreen)
        g.push_state()
        launch()
        
        def game_loop():
            game = GetGame()
            while GetGame() is game:
                GetGame().main(clock, fps)
                if len(pygame.event.get([pygame.QUIT])) > 0:
                    GetGame().quit = True
                if GetGame().__class__.__name__ == "NewGame":
                    GetGame().quit = True
        
        while not GetGame().quit:
            game = GetGame()
            game_loop()
                
        pygame.quit()

    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()
