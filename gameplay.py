#!/usr/bin/env python
# gameplay.py
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

import math
import sqlite3

class UserGame(object):

    """Abstraction of database connection for a user
    
    Allows game engine to set values on certain levels and returns values in a
    form the game can read.

    Initilize the object and set what random things stand for, this module
    excepts all errors from sqlite and converts them to one for initilizing:
        DatabaseError
    and one for more spesific things:
        QueryError
    If you reach a database error, that means that you are unable to open the
    database, this is bad, because no further options can be performed, except
    ensure the database is intact
    On the other hand QueryError is quite usefull, because in most cases you
    just want to skip the current operation and try a different one, but in some
    cases you will need to quit.

    Next, when you init the object, you can expect a DatabaseError, but since
    once you open it once you can expect it to open again, the next time you
    will get a query error even if you are unable to reach the database, but
    DatabaseError will be part of that error
    
    """

    def __init__(self):
        super(UserGame, self).__init__()
        self.arg = arg
        
    def stageloop(self, list):
        """Make the stage for the user based one cornflaks"""
        self.delimiter('.')
        self.cursor = 0
        self.lastdelimeter = 0
        self.output = []
        self.list = list
        try:
            if self.list[self.cursor] == self.delimiter:
                if self.list

        except Exception, e:
            raise e
        else:
            pass
                
