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
from optparse import OptionParser
import csv

def filetogameplay(file, db, force):
    """convert from a enter seperated file to """
    pass

def csvtolevels(file, db, force):
    """docstring for csvtolistoflists"""

    createDb = sqlite3.connect(db)
    queryCurs = createDb.cursor()
    list = csv.reader(open(file))
    dbmade = False
    try:
        queryCurs.execute('''create table levels(
                            ID INTEGER PRIMARY KEY,
                            grade INTAGER,
                            stage INTAGER,
                            level INTAGER,
                            allmath INTAGER,
                            database TEXT,
                            acomplishment TEXT,
                            acomcount INTAGER,
                            playcount INTAGER)
                          ''')

    except sqlite3.OperationalError, e:
        if force:
            queryCurs.execute('''drop table levels''')
            queryCurs.execute('''create table levels(
                                ID INTEGER PRIMARY KEY,
                                grade INTAGER,
                                stage INTAGER,
                                level INTAGER,
                                allmath INTAGER,
                                database TEXT,
                                acomplishment TEXT,
                                acomcount INTAGER,
                                playcount INTAGER)
                              ''')
            dbmade = True
        else:
            print 'Cannot overwrite table, use --force (-f)'
    else:
        dbmade = True

    if dbmade:
        for i in list:
            queryCurs.execute('''insert into levels (grade, stage, level,
                              allmath, database, acomplishment, acomcount,
                              playcount)values (?, ?, ?, ?, ?, ?, ?, ?)''',i)
        createDb.commit()
        queryCurs.close()


            
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--force", action="store_true",
                      dest="force", default=False, 
                      help="Overwrite existing file.")
    parser.add_option("-o", "--output", type="string", dest="db",
                      default='out.db',
                      help="The database to output to")
    parser.add_option("-g", "--gameplay", type="string", dest="gameplay", default=None,
                      help="The Gameplay CSV to import")
    parser.add_option("-l", "--levels", type="string", dest="levels", default=None,
                      help="The Levels CSV to import")

    (options, args) = parser.parse_args()
    csvtolevels(options.levels, options.db, options.force)
    filetogameplay(options.gameplay, options.db, options.force)
