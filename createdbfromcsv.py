#!/usr/bin/env python
# createdbfromcsv.py
# Copyright (C) 2011 Mark Amber
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

import sqlite3
import os
import optparse as OptionParser

def csvtolistoflists(file):
    """docstring for csvtolistoflists"""
    pass

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--fullscreen", action="store_true",
                      dest="fullscreen", default=False, help="Overwrite\
                      existing file.")
    parser.add_option("-r", "--resolution", type="int", nargs=2, dest="res", help="Specify the resolution. Default is 0 0, which uses the screen's resolution.", metavar="WIDTH HEIGHT", default=(0,0))
    parser.add_option("-s", "--fps", type="int", dest="fps", help="Specify the fps cap. Default is 30", metavar="FPS", default=30)
    parser.add_option("-p", "--profile", action="store_true", default=False, dest="profile", help="Enable profiling. pstats files will made for each GameState in profiles/")
    parser.add_option("-o", "--output", type="string", dest="profile_output", default=None, help="Specify an output directory for profiling data")
    (options, args) = parser.parse_args()
