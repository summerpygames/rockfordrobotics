from random import choice, randint
from math import sqrt, ceil

def generate():
    """Adding two numbers to a maximum sum of 100."""
    term1, term2, right = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right)
    return (term1, '+', term2, right, wrong1, wrong2, wrong3, 'standard')
    
def generate_question():
    """This is generating the three terms involved in the sum."""
    right = choice(range(11,101))
    term11, term21 = [0,0]
    while term11 + term21 < 10 and int(str(term11+term21)[-1]) != int(str(right)[-1]):
        term11 = choice(range(1,10))
        term21 = choice(range(1,10))
    term12 = choice(range(1,int(ceil(float(right)/10))))
    term1 = 10*term12 + term11
    term22 = right - term1 - term21
    term2 = term22 + term21
    return (term1, term2, right)

def generate_wrong(term1, term2, right):
    """Giving many wrong answers to choose from."""
    wrongs = []
    wrongs.append(right + 1)
    wrongs.append(abs(right - 1))
    wrongs.append(right + 2)
    wrongs.append(abs(right - 2))
    wrongs.append(30*int(sqrt(right)))
    wrongs.append(right + 10)
    wrongs.append(abs(right - 10))
    wrongs.append(right + 20)
    wrongs.append(abs(right - 20))
    wrongs.append(randint(10, 100))
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
