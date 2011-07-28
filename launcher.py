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

virtual_size = (1200,900)
color = (0,0,0)

def launch():
    # Here we go for where we can put some launching code
    g = menu.MainMenu()
    g.push_state()

def format_columns(message, data, file = None):
    first_width = max([len(x[0]) for x in data])
    second_width = max([len(x[1]) for x in data])

    # calculate a format string for the output lines
    format_str= "%%-%ds        %%-%ds" % (first_width, second_width)

    if file is None:
        print message
        print "=" * (first_width + second_width + 8)
        for x in data:
            print format_str % x
    else:
        f = open(file, "w")
        format_str = format_str + "\n"
        f.write(message + "\n")
        f.write("=" * (first_width + second_width + 8) + "\n")
        for x in data:
            f.write(format_str % x)
        f.close()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--fullscreen", action="store_true", dest="fullscreen", default=False, help="Run in fullscreen mode. Default is windowed mode.")
    parser.add_option("-r", "--resolution", type="int", nargs=2, dest="res", help="Specify the resolution. Default is 0 0, which uses the screen's resolution.", metavar="WIDTH HEIGHT", default=(0,0))
    parser.add_option("-s", "--fps", type="int", dest="fps", help="Specify the fps cap. Default is 30", metavar="FPS", default=30)
    parser.add_option("-p", "--profile", action="store_true", default=False, dest="profile", help="Enable profiling. pstats files will made for each GameState in profiles/")
    parser.add_option("-o", "--output", type="string", dest="profile_output", default=None, help="Specify an output directory for profiling data")
    (options, args) = parser.parse_args()

    resolution = options.res
    fps = options.fps
    fullscreen = options.fullscreen

    if olpcgames.ACTIVITY:
        resolution = olpcgames.ACTIVITY.game_size
        virtual_size = olpcgames.ACTIVITY.game_size
        fps = 20
        fullscreen = False
    
    if options.profile_output is not None:
        output_dir = options.profile_output
    else:
        d = time.strftime("%d-%m-%Y %H-%M-%S")
        output_dir = os.path.join('profiles', d)
    if options.profile:
        try:
            os.mkdir(output_dir)
        except OSError:
            pass
    
    ## Let's output some friendly information at the top
    output = [
        ("resolution:", "Autodetect" if options.res == (0,0) else str(options.res[0]) + " x " + str(options.res[1])),
        ("fullscreen:", "True" if options.fullscreen else "False"),
        ("FPS:", str(options.fps)),
        ("profiling:", ("True" if options.profile else "False")),
        ]
    if options.profile:
        output.append(("profile output directory", output_dir))
    output.append(("switches: ", " ".join(sys.argv[1:])))
    format_columns("summerpygames test launcher", output)
    if options.profile:
        format_columns("summerpygames test launcher config", output, os.path.join(output_dir, "config.txt"))
            
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
        
        profiles = {}
        while not GetGame().quit:
            game = GetGame()
            if options.profile:
                if game in profiles:
                    profiles[game] = profiles[game] + 1
                else:
                    profiles[game] = 1
                try:
                    os.mkdir(os.path.join(output_dir, game.__class__.__module__))
                except OSError:
                    pass
                cProfile.run('game_loop()', os.path.join(output_dir, game.__class__.__module__, game.__class__.__name__ + "_" + str(profiles[game]) + ".pstats"))
            else:
                game_loop()
                
            # Let's print some FPS information out
            avg_fps = sum(game.fps_log) / float(len(game.fps_log))
            stddev = sqrt(sum((avg_fps - x) ** 2 for x in game.fps_log) / float(len(game.fps_log)))
            
            output = [
                ("Minimum fps:", str(min(game.fps_log))),
                ("Maximum fps:", str(max(game.fps_log))),
                ("Average fps:", str(avg_fps)),
                ("Standard deviation:", str(stddev))
                ]
            format_columns(game.__class__.__name__ + " Framerate Statistics", output)
            if options.profile:
                format_columns(game.__class__.__name__ + " Framerate Statistics", output, os.path.join(output_dir, game.__class__.__module__, game.__class__.__name__ + "_" + str(profiles[game]) + ".framestats"))
        pygame.quit()
    except KeyboardInterrupt:
        pygame.quit()
