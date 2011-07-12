from random import choice, randint
from math import sqrt

def generate():
    """Adding two numbers to a maximum sum of 20."""
    term1, term2, right = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right)
    term1 *= 10
    term2 *= 10
    right *= 10
    wrong1 *= 10
    wrong2 *= 10
    wrong3 *= 10
    return (term1, term2, right, wrong1, wrong2, wrong3)

def generate_question():
    """This is generating the three terms involved in the sum."""
    right = choice(range(1,11))
    term2 = choice(range(1,right+1))
    term1 = right - term2
    return (term1, term2, right)

def generate_wrong(term1, term2, right):
    """Giving many wrong answers to choose from."""
    wrongs = []
    wrongs.append(right + 1)
    wrongs.append(right - 1)
    wrongs.append(right + 2)
    wrongs.append(right - 2)
    wrongs.append(2*int(sqrt(right)))
    wrongs.append(randint(1, 10))
    wrongs.append(randint(1, 10))
    wrongs.append(randint(1, 10))
    wrongs.append(randint(1, 10))
    wrongs.append(randint(1, 10))
    
    the_wrong_3 = []

    for i in range(3):
        tmp = choice(wrongs)
        wrongs.remove(tmp)
        if tmp not in the_wrong_3 and tmp is not right:
            the_wrong_3.append(tmp)
    return the_wrong_3