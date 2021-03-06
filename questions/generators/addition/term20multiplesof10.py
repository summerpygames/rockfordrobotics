from random import choice, randint
from math import sqrt

def generate():
    """Adding two numbers to a maximum sum of 120."""
    term1, term2, right = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right)
    return (term1, '+', term2, right, wrong1, wrong2, wrong3, 'standard')
    
def generate_question():
    """This is generating the three terms involved in the sum."""
    term1 = choice(range(1,21))
    term2 = 10*choice(range(1,11))
    right = term1 + term2
    return (term1, term2, right)

def generate_wrong(term1, term2, right):
    """Giving many wrong answers to choose from."""
    wrongs = []
    wrongs.append(right + 10)
    wrongs.append(abs(right - 10))
    wrongs.append(right + 20)
    wrongs.append(abs(right - 20))
    wrongs.append(9*int(sqrt(right)))
    wrongs.append(randint(1, 120))
    wrongs.append(randint(1, 120))
    wrongs.append(randint(1, 120))
    wrongs.append(randint(1, 120))
    wrongs.append(randint(1, 120))
    
    the_wrong_3 = []

    while len(the_wrong_3) < 3:
        if len(wrongs) > 0:
            tmp = choice(wrongs)
            wrongs.remove(tmp)
        else: # This should never happen, if it does, you have a problem.
            tmp = randint(-7, -1)
        if tmp not in the_wrong_3 and tmp is not right:
            the_wrong_3.append(tmp)
    return the_wrong_3
