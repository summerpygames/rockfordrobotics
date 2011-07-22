from random import choice, randint
from math import sqrt

def generate():
    """subtracting two numbers to a maximum difference of 999."""
    term1, term2, right = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right)
    return (term1, '-', term2, right, wrong1, wrong2, wrong3, 'standard')
    
def generate_question():
    """This is generating the three terms involved in the difference."""
    right = randint(10,999)
    term1 = randint(right,1000)
    term2 = term1 - right
    regroup = 0
    while regroup == 0:
        for i in range(len(str(term1))):
            if i in range(len(str(term2))):
                i += 1
                if int(str(term1)[-i]) < int(str(term2)[-i]):
                    regroup = 1
                    break
            else: break
        if regroup == 0:
            term1 = randint(right,1000)
            term2 = term1 - right
    return (term1, term2, right)

def generate_wrong(term1, term2, right):
    """Giving many wrong answers to choose from."""
    wrongs = []
    wrongs.append(right + 1)
    wrongs.append(abs(right - 1))
    wrongs.append(right + 2)
    wrongs.append(abs(right - 2))
    wrongs.append(8*int(sqrt(right)))
    wrongs.append(right + 10)
    wrongs.append(abs(right - 10))
    wrongs.append(right + 20)
    wrongs.append(abs(right - 20))
    wrongs.append(randint(0,9990))
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