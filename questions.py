import random

points=0

def getnum(level=0, numrange=None):
    '''Random Number generator
    use the first argument, level, to select level, 1 or 2
    use the second argument as a keyword, numrange, to override that
    
    getnum(1) returns random 1-6
    getnum(2) returns random 1-12
    getnum(numrange=[7,32]) returns random 7-32
    '''
    if level is 1 and numrange is None:
        # If you're onlu on level one, only numbers 1 through 6
        numrange = [1,6]
    
    elif level is 2 and numrange is None:
        # If you're on level two, return numbers 1 through 12
        numrange = [1,12]

    elif level is 0 and numrange is not None:
        # Set the numrange to a new fangled coustomised range 
        numrange = numrange

    else:
        # Uh Oh, trouble, exactly one argument will be used
        raise IOError('level xor numrange please!')
    
    return random.randint(numrange[0], numrange[1])

def question(operation, difficulty):
    '''Create a question for the user and return a tuple.

    the argument operation is for choosing what type of arithmatic
        1 = Addition
        2 = Subtraction
        3 = Multiplication
        4 = Devision
    the argument difficulty is for the size of numbers to deal with and possible non positive integer answers
    
    return is in format (term_1, term_2, result, operation, operation_difficulty, possibly_remainder)
    '''

    if operation not in range(1,5):
        raise IOError('operation is 1-4')

    if difficulty not in range(1,3):
        raise IOError('difficulty is 1-2')

    if operation is 1:
        # Addition, the result is the SUM
        term_1 = getnum(difficulty)
        term_2 = getnum(difficulty)
        result = term_1 + term_2
        return (term_1, term_2, result, 1, 1)

    elif operation is 2:
        # Subtraction, the result is the Difference
        term_1 = getnum(difficulty)
        term_2 = getnum(difficulty)
        if difficulty is 1:
            while term_2 > term_1:
                term_1 = getnum(difficulty)
                term_2 = getnum(difficulty)
            result = term_1 - term_2
            return (term_1, term_2, result, 2, 1)
        else:
            if term_2 <= term_1:
                operation_difficulty = 2
            else:
                operation_difficulty = 1
            
            result = term_1 - term_2
            return (term_1, term_2, result, 2, operation_difficulty)

    elif operation is 3:
        # Multiplication, the result is the quotient
        term_1 = getnum(difficulty)
        term_2 = getnum(difficulty)
        result = term_1 * term_2
        return (term_1, term_2, result, 3, 1)

    elif operation is 4:
        # Division, the result is a quotient
        term_1 = getnum(difficulty)
        term_2 = getnum(difficulty)
        while term_1 > term_2:
            term_1 = getnum(difficulty)
            term_2 = getnum(difficulty)
        if difficulty is 1:
            while term_1 % term_2 != 0:
                term_1 = getnum(difficulty)
                term_2 = getnum(difficulty)
            result = term_1 / term_2
            return (term_1, term_2, result, 4, 1)
        else:
            result = term_1 / term_2
            remainder = term_1 % term_2
            return (term_1, term_2, result, 4, 2)

    else:
        # Nothing to do here, no way this will happen
            
