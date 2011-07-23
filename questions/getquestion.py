'''
File: getquestion.py
Author: Mark Amber
Description: Give a random question back
'''
import shelve
import os
import random

userStrings = ['addition.upto10', 'addition.upto18', 'addition.upto20', 'addition.fracabove1', 'addition.fracbelow1', 'addition.multiplesof10', 'addition.term20multiplesof10', 'addition.regroup100', 'addition.regroup1000', 'addition.noregroup100', 'addition.noregroup1000', 'subtraction.upto10', 'subtraction.upto18', 'subtraction.upto20', 'subtraction.fracabove1', 'subtraction.fracbelow1', 'subtraction.multipleof5', 'subtraction.upto20multipleof5', 'subtraction.regroup100', 'subtraction.regroup1000', 'subtraction.noregroup100', 'subtraction.noregroup1000', 'multiplication.upto18', 'multiplication.upto36', 'multiplication.upto72', 'multiplication.upto1000', 'multiplication.fractions', 'division.upto5', 'division.longdivision', 'division.shortdivision']

sourceStrings = ['addition.upto10.shelve.db', 'addition.upto18.shelve.db', 'addition.upto20.shelve.db', 'addition.fracabove1.shelve.db', 'addition.fracbelow1.shelve.db', 'addition.multiplesof10.shelve.db', 'addition.term20multiplesof10.shelve.db', 'addition.regroup100.shelve.db', 'addition.regroup1000.shelve.db', 'addition.noregroup100.shelve.db', 'addition.noregroup1000.shelve.db', 'subtraction.upto10.shelve.db', 'subtraction.upto18.shelve.db', 'subtraction.upto20.shelve.db', 'subtraction.fracabove1.shelve.db', 'subtraction.fracbelow1.shelve.db', 'subtraction.multipleof5.shelve.db', 'subtraction.upto20multipleof5.shelve.db', 'subtraction.regroup100.shelve.db', 'subtraction.regroup1000.shelve.db', 'subtraction.noregroup100.shelve.db', 'subtraction.noregroup1000.shelve.db', 'multiplication.upto18.shelve.db', 'multiplication.upto36.shelve.db', 'multiplication.upto72.shelve.db', 'multiplication.upto1000.shelve.db', 'multiplication.fractions.shelve.db', 'division.upto5.shelve.db', 'division.longdivision.shelve.db', 'division.shortdivision.shelve.db']

u, s = userStrings, sourceStrings

def get(type):
    """Return the dict of a rondom question from requested entry"""
    questionNum = random.randint(1, 1000)
    source = s[u.index(type)]
    database = shelve.open(os.path.join('questions',
                                        'databases',
                                        source),
                           writeback = False)
    return database[str(questionNum)]
    
if __name__ == '__main__':
    question = get()
    print question['term1'], question['operation'], question['term2'],
    question['right'], question['wrong1'], question['wrong2'],
    question['wrong3'], question['type']
