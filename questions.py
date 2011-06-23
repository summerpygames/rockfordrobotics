import random

points=0

def getnum1(level=0, numrange=None):
    """Random Number generator
    use the first argument, level, to select level, 1 or 2
    use the second argument as a keyword, numrange, to override that
    
    getnum(1) returns random 1-6
    getnum(2) returns random 1-12
    getnum(numrange=[7,32]) returns random 7-32
    """
    if level is 1 and numrange is None:
        # If you're onlu on level one, only numbers 1 through 6
        numrange = [0, 1, 3, 2, 4, 6, 5, 1, 3, 0, 5, 2, 4, 6, 6, 1, 0, 5, 2, 3, 4, 1, 6,
                   5, 4, 3, 0, 2]
    elif level is 2 and numrange is None:
        # If you're on level two, return numbers 1 through 12
        numrange = [0, 1, 3, 5, 7, 9, 2, 4, 0, 6, 8, 10, 2, 9, 3, 8, 4, 7, 5, 6, 1,
                    10, 10, 7, 4, 5, 3, 2, 0, 1, 9, 8, 6]

    elif level is 0 and numrange is not None:
        # Set the numrange to a new fangled coustomised range 
        numrange = numrange

    else:
        # Uh Oh, trouble, exactly one argument will be used
        raise IOError('level xor numrange please!')
    
    return random.choice(numrange)

def getnum2(level=0, numrange=None):
    """Random Number generator
    use the first argument, level, to select level, 1 or 2
    use the second argument as a keyword, numrange, to override that
    
    getnum(1) returns random 1-6
    getnum(2) returns random 1-12
    getnum(numrange=[7,32]) returns random 7-32
    """
    if level is 1 and numrange is None:
        # If you're onlu on level one, only numbers 1 through 6
        numrange = [5, 4, 2, 1, 3, 0, 6, 2, 5, 1, 4, 3, 6, 0, 0, 5, 6, 3, 4, 1,
                   2, 3, 4, 5, 2, 1, 6, 0]
    elif level is 2 and numrange is None:
        # If you're on level two, return numbers 1 through 12
        numrange = [8, 3, 7, 1, 2, 6, 4, 9, 5, 0, 10, 1, 4, 7, 0, 2, 5, 8, 3, 6,
                   9, 7, 8, 2, 3, 5, 6, 4, 9, 0, 1, 10]

    elif level is 0 and numrange is not None:
        # Set the numrange to a new fangled coustomised range 
        numrange = numrange

    else:
        # Uh Oh, trouble, exactly one argument will be used
        raise IOError('level xor numrange please!')
    
    return random.choice(numrange)

def getnum2_withoutzero(level=0, numrange=None):
    """Random Number generator
    use the first argument, level, to select level, 1 or 2
    use the second argument as a keyword, numrange, to override that
    
    getnum(1) returns random 1-6
    getnum(2) returns random 1-12
    getnum(numrange=[7,32]) returns random 7-32
    """
    if level is 1 and numrange is None:
        # If you're onlu on level one, only numbers 1 through 6
        numrange = [5, 4, 2, 1, 3, 6, 2, 5, 1, 4, 3, 6, 5, 6, 3, 4, 1,
                   2, 3, 4, 5, 2, 1, 6]
    elif level is 2 and numrange is None:
        # If you're on level two, return numbers 1 through 12
        numrange = [8, 3, 7, 1, 2, 6, 4, 9, 5, 10, 1, 4, 7, 2, 5, 8, 3, 6,
                   9, 7, 8, 2, 3, 5, 6, 4, 9, 1, 10]

    elif level is 0 and numrange is not None:
        # Set the numrange to a new fangled coustomised range 
        numrange = numrange

    else:
        # Uh Oh, trouble, exactly one argument will be used
        raise IOError('level xor numrange please!')
    
    return random.choice(numrange)



def wrong_answer(term_1, term_2, operation, operation_difficulty=1):
    """This will output a list with three wrong answers"""
    wrongs = []
    if operation is 1:
        # Addition, generate some bad answers
        wrongs.add(term_1 + term_2 + 1)
        wrongs.add(term_1 + term_2 - 1)
        wrongs.add(term_1 + term_2 + 2)
        wrongs.add(term_1 + term_2 - 2)
        wrongs.add(term_1 + term_2 + 3)
        wrongs.add(term_1 * term_2)
        wrongs.add(term_1 - term_2)
        wrongs.add(random.randomint(1,20))
    if operation is 2:
        # Subtraction, generate some bad answers
        wrongs.add(term_1 + term_2 + 1)
        wrongs.add(term_1 + term_2 - 1)
        wrongs.add(term_1 + term_2 + 2)
        wrongs.add(term_1 + term_2 - 2)
        wrongs.add(term_1 + term_2 + 3)
        wrongs.add(term_1 * term_2)
        wrongs.add(term_1 - term_2)
        wrongs.add(random.randomint(1,22))
    if operation is 3:
        # Multiplication, generate some bad anwsers
        wrongs.add(term_1 * (term_2 + 1))
        wrongs.add(term_1 * (term_2 - 1))
        wrongs.add(term_1 + term_2)
        wrongs.add((term_1 + 1) * term_2)
        wrongs.add((term_1 - 1) * term_2)
        wrongs.add((term_1 + 2) * term_2)
        wrongs.add(term_1 - term_2)
        wrongs.add(random.randomint(1,20))
    if operation is 4 and operation_difficulty is 1:
        try:
            wrongs.add(term_1 / (term_2 + 1))
            wrongs.add(term_1 / (term_2 + 2))
            wrongs.add(term_1 * term_2)
            wrongs.add(term_1 / (term_2 - 1))
            wrongs.add(term_1 / (term_2 - 2))
            wrongs.add(term_1 - term_2)
            wrongs.add(random.randomint(1,10))
            wrongs.add(term_1 + term_2)
        except ZeroDivisionError:
            wrong_answer(term_1, term_2 + 1, operation, operation_difficulty)
    
    if operation is 4 and operation_difficulty is 2:
        try:
            wrongs.add([(term_1 / term_2), (term_1 % term_2) + 1])
            wrongs.add([(term_1 / term_2), (term_1 % term_2) - 1])
            wrongs.add([(term_1 / term_2 + 1), (term_1 % term_2)])
            wrongs.add([(term_1 / term_2 + 2), (term_1 % term_2)])
            wrongs.add([(term_1 / term_2 - 1), (term_1 % term_2)])
            wrongs.add([(term_1 / term_2 - 2), (term_1 % term_2)])
            wrongs.add([(term_1 / term_2), random.randomint(1, 20)])
        except  ZeroDivisionError:
            wrong_answer(term_1, term_2 + 1 operation, operation_difficulty)

    


def question(operation, difficulty):
    """Create a question for the user and return a tuple.

    the argument operation is for choosing what type of arithmatic
        1 = Addition
        2 = Subtraction
        3 = Multiplication
        4 = Devision
    the argument difficulty is for the size of numbers to deal with and possible non positive integer answers
    
    return is in format (term_1, term_2, result, operation, operation_difficulty, possibly_remainder)
    """

    if operation not in range(1,5):
        raise IOError('operation is 1-4')

    if difficulty not in range(1,3):
        raise IOError('difficulty is 1-2')

    if operation is 1:
        # Addition, the result is the SUM
        term_1 = getnum1(difficulty)
        term_2 = getnum2(difficulty)
        result = term_1 + term_2
        return (term_1, term_2, result, 1, 1)

    elif operation is 2:
        # Subtraction, the result is the Difference
        term_1 = getnum1(difficulty)
        term_2 = getnum2(difficulty)
        if difficulty is 1:
            while term_2 > term_1:
                term_1 = getnum1(difficulty)
                term_2 = getnum2(difficulty)
            result = term_1 - term_2
            return (term_1, term_2, result, 2, 1)
        else:
            if term_2 >= term_1:
                operation_difficulty = 2
            else:
                operation_difficulty = 1
            
            result = term_1 - term_2
            return (term_1, term_2, result, 2, operation_difficulty)

    elif operation is 3:
        # Multiplication, the result is the quotient
        term_1 = getnum1(difficulty)
        term_2 = getnum2(difficulty)
        result = term_1 * term_2
        return (term_1, term_2, result, 3, 1)

    elif operation is 4:
        try:

            # Division, the result is a quotient
            term_1 = getnum1(difficulty)
            term_2 = getnum2_withoutzero(difficulty)
            while term_2 > term_1:
                term_1 = getnum1(difficulty)
                term_2 = getnum2_withoutzero(difficulty)
            if difficulty is 1:
                while term_1 % term_2 != 0:
                    term_1 = getnum1(difficulty)
                    term_2 = getnum2_withoutzero(difficulty)
                result = term_1 / term_2
                return (term_1, term_2, result, 4, 1)
            else:
                result = term_1 / term_2
                remainder = term_1 % term_2
                return (term_1, term_2, result, 4, 2, remainder)
        except ZeroDivisionError:
            question(operation, difficulty)

    else:
        pass
        # Nothing to do here, no way this will happen
            
