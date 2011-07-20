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

sources = [addition.upto10, addition.upto18, addition.upto20, addition.fracabove1, addition.fracbelow1, addition.multiplesof10, addition.term20multiplesof10, addition.regroup100, addition.regroup1000, addition.noregroup100, addition.noregroup1000, subtraction.upto10, subtraction.upto18, subtraction.upto20, subtraction.fracabove1, subtraction.fracbelow1, subtraction.multipleof5, subtraction.upto20multipleof5, subtraction.regroup100, subtraction.regroup1000, subtraction.noregroup100, subtraction.noregroup1000, multiplication.upto18, multiplication.upto36, multiplication.upto72, multiplication.upto1000, multiplication.fractions, division.upto5, division.longdivision, division.shortdivision]

questionNum = 0

def addQuestion(database, source):
    question = {}
    global questionNum
    questionNum += 1
    question['term1'], question['operation'], question['term2'], question['right'], question['wrong1'], question['wrong2'], question['wrong3'], question['type'] = source.generate()
#       The 'operation' is either '+', '-', '*', or '/'.
#       The 'type' is either standard, fraction, or remainder. It reflects on the way the terms are put together.
    database[questionNum] = question
    return

def getQuestion(number):
    database = shelve.open('questions.dat', writeback = True)
    toreturn = []
    for i in database[number]:
        toreturn.append(database[number][i])
    return toreturn
    database.close()

def main(): #This should only be run once: upon startup of the game.
    database = shelve.open('questions.dat', writeback = True)
    for source in sources:
        for i in range(1000):
            addQuestion(database, source)
    database.close()