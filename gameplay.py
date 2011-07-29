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
from random import choice

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

    def __init__(self, db):
        super(UserGame, self).__init__()
        self.db = sqlite3.connect(db)
        self.c = self.db.cursor()
        
    def get_db(self):
        """returns the database"""
        return self.db

    def close(self):
        self.c.close()

    def get_gameplay(self):
        gameplays = []
        self.c.execute('''
                        SELECT id from gameplay
                       ''')
        for row in self.c:
            gameplays.append(row[0])

        self.c.execute('''
                       SELECT gameplay FROM gameplay
                       WHERE id=?
                       ''', (choice(gameplays),)
                       )
        for row in self.c:
            gameplay = row[0]
        
        return list(str(gameplay))

    def get_game_levels(self, grade, stage):
        """This will return an ID, a Description of the level, and if its
        unlocked, and if it is played"""
        levels = []
        self.c.execute('''
                       SELECT id, level, description, playcount FROM levels
                       WHERE grade=? AND stage=? AND allmath=0
                       ''', (grade, stage)
                       )
        for row in self.c:
            levels.append({'id':row[0], 'level':row[1], 'description':row[2],
                           'playcount':row[3]})
        
        return levels

    def get_math_levels(self, grade, stage):
        """This will return an ID, a Description of the level, and if its
        unlocked, and if it is played"""
        levels = []
        self.c.execute('''
                       SELECT id, level, description, playcount FROM levels
                       WHERE grade=? AND stage=? AND allmath=1
                       ''', (grade, stage)
                       )
        for row in self.c:
            levels.append({'id':row[0], 'level':row[1], 'description':row[2],
                           'playcount':row[3]})
        
        return levels


    def getlevel(self, id):
        """Get information on a certain level"""
        self.c.execute('''
                       SELECT id, database, allmath FROM levels
                       WHERE id=?
                       ''', (str(id))
                       )
        for row in self.c:
            print row[2]
            id, databasefile, allmath = int(row[0]), str(row[1]),\
                                            bool(int(row[2]))

        gameplaylist = self.get_gameplay() if allmath else\
        ['.','A','_','2','0','.'] # in the case that it is math
        return (databasefile, gameplaylist) 

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
                
