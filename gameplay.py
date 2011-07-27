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
import pdb

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

    def __init__(self, db, ):
        super(UserGame, self).__init__()
        createDb = sqlite3.connect(db)
        queryCurs = createDb.cursor()
        

    def getlevels(self, grade, stage):
        """This will return an ID, a Description of the level, and if its
        unlocked, and if it is played"""

        return (id, description, unlocked, played)
        
    def stageloop(self, l):
        """Make the stage for the user based one cornflaks"""
        self.delimiter = '.'
        self.cursor = 0
        self.lastdelimeter = 0
        self.output = []
        self.list = list(l)
        self.running = True
        while self.running == True:
            try:
                if self.list[self.cursor] == self.delimiter:
                    try:
                        int(self.list[self.cursor + 1])
                    except ValueError, e:
                        self.lastdelimeter = self.cursor
                    else:
                        self.cursor += 1
                        startnumber = self.cursor 
                        stillnumber = True
                        number = int(self.list[self.cursor])
                        self.cursor += 1
                        while stillnumber == True:
                            try: # See if the next thing in the list is a number
                                int(self.list[self.cursor])
                            except ValueError, e: # if it is say a period
                                stillnumber = False
                            else: # If the next thing is still a number
                                number = (number*10) +\
                                int(self.list[self.cursor])
                                self.cursor += 1
                                #Now we make the number one digit longer
                        self.list[startnumber:self.cursor] = list(str(number-1)) if number != 0\
                                                             else []
                        self.cursor = self.lastdelimeter
                    finally:
                        self.cursor += 1

                elif self.list[self.cursor] == 'A':
                    self.output.append('ask')
                    self.cursor += 1
                elif self.list[self.cursor] == 'E':
                    try:
                        int(self.list[self.cursor + 1])
                    except ValueError, e:
                        pass
                    else:
                        self.cursor += 1
                        self.output.append(int(self.list[self.cursor]))
                    finally:
                        self.cursor += 1
                else:
                    self.cursor += 1

            except IndexError, e:
                return self.output
                self.running = False
                
