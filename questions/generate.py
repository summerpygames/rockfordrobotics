# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 22:49:20 2011

@author: lucas
"""
import shelve
import addition.upto10
import addition.upto18
import addition.upto20
import addition.fracabove1
import addition.fracbelow1
import addition.multiplesof10
import addition.term20multiplesof10
import addition.regroup100
import addition.regroup1000
import addition.noregroup100
import addition.noregroup1000
import subtraction.upto10
import subtraction.upto18
import subtraction.upto20
import subtraction.fracabove1
import subtraction.fracbelow1
import subtraction.multipleof5
import subtraction.upto20multipleof5
import subtraction.regroup100
import subtraction.regroup1000
import subtraction.noregroup100
import subtraction.noregroup1000
import multiplication.upto18
import multiplication.upto36
import multiplication.upto72
import multiplication.upto1000
import multiplication.fractions
import division.upto5
import division.longdivision
import division.shortdivision
import os
sources = [addition.upto10, addition.upto18, addition.upto20, addition.fracabove1, addition.fracbelow1, addition.multiplesof10, addition.term20multiplesof10, addition.regroup100, addition.regroup1000, addition.noregroup100, addition.noregroup1000, subtraction.upto10, subtraction.upto18, subtraction.upto20, subtraction.fracabove1, subtraction.fracbelow1, subtraction.multipleof5, subtraction.upto20multipleof5, subtraction.regroup100, subtraction.regroup1000, subtraction.noregroup100, subtraction.noregroup1000, multiplication.upto18, multiplication.upto36, multiplication.upto72, multiplication.upto1000, multiplication.fractions, division.upto5, division.longdivision, division.shortdivision]

sourceStrings = ['addition.upto10.shelve.db', 'addition.upto18.shelve.db', 'addition.upto20.shelve.db', 'addition.fracabove1.shelve.db', 'addition.fracbelow1.shelve.db', 'addition.multiplesof10.shelve.db', 'addition.term20multiplesof10.shelve.db', 'addition.regroup100.shelve.db', 'addition.regroup1000.shelve.db', 'addition.noregroup100.shelve.db', 'addition.noregroup1000.shelve.db', 'subtraction.upto10.shelve.db', 'subtraction.upto18.shelve.db', 'subtraction.upto20.shelve.db', 'subtraction.fracabove1.shelve.db', 'subtraction.fracbelow1.shelve.db', 'subtraction.multipleof5.shelve.db', 'subtraction.upto20multipleof5.shelve.db', 'subtraction.regroup100.shelve.db', 'subtraction.regroup1000.shelve.db', 'subtraction.noregroup100.shelve.db', 'subtraction.noregroup1000.shelve.db', 'multiplication.upto18.shelve.db', 'multiplication.upto36.shelve.db', 'multiplication.upto72.shelve.db', 'multiplication.upto1000.shelve.db', 'multiplication.fractions.shelve.db', 'division.upto5.shelve.db', 'division.longdivision.shelve.db', 'division.shortdivision.shelve.db']

questionNum = 0

def addQuestion(database, source):
    question = {}
    global questionNum
    questionNum += 1
    question['term1'], question['operation'], question['term2'], question['right'], question['wrong1'], question['wrong2'], question['wrong3'], question['type'] = source.generate()
#       The 'operation' is either '+', '-', '*', or '/'.
#       The 'type' is either 'standard', 'fraction', or 'remainder'. It reflects on the way the terms are put together.
    database[str(questionNum)] = question
    return question
    
def main(): #This should only be run once: upon startup of the game.
    for sourceString in sourceStrings:
        global questionNum
        questionNum = 0
        database = shelve.open(os.path.join('questions', 'databases',sourceString), writeback = True)
        source = sources[sourceStrings.index(sourceString)]
        for i in range(1000):
            addQuestion(database, source)
        database.close()
