import random
from math import sqrt

def generate():
    """Adding two numbers to a maximum sum of 1000."""
    term1, term2, right = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right)
    return (term1, term2, right, wrong1, wrong2, wrong3)
    
def generate_question():
    """This is generating the three terms involved in the sum."""
    right = random.choice(range(1,1001))
    term1 = random.choice(range(right,1001))
    term2 = term1 - right
    if term2 > term1:
        term3 = term1
        term1 = term2
        term2 = term3
    for i in range(len(str(term1))):
        i += 1
        while int(str(term1)[-i]) < int(str(term2)[-i]):
            str(term1)[-i] = str(random.choice(range(int(str(right)[-i]),10)))
            str(term2)[-i] = str(int(str(term1)[-i]) - int(str(right)[-i]))
            change = True
        if change and i is not len(str(term1)):
            term2 += 10**i
        elif change:
            #This shouldn't happen
            print term1, term2, right, "--What's wrong?"
    if term2 > term1:
        term3 = term1
        term1 = term2
        term2 = term3
    return (term1, term2, right)
    if term2 > term1:
        term3 = term1
        term1 = term2
        term2 = term3
def generate_wrong(term1, term2, right):
    """Giving many wrong answers to choose from."""
    wrongs = []
    wrongs.append(right + 1)
    wrongs.append(right - 1)
    wrongs.append(right + 2)
    wrongs.append(right - 2)
    wrongs.append(30*int(sqrt(right)))
    wrongs.append(right + 10)
    wrongs.append(right - 10)
    wrongs.append(right + 20)
    wrongs.append(right - 20)
    wrongs.append(random.randint(100, 1000))
    the_wrong_3 = []

    while len(the_wrong_3) < 3:
        if len(wrongs) > 0:
            tmp = random.choice(wrongs)
            wrongs.remove(tmp)
        else: # This should never happen, if it does, you have a problem.
            tmp = random.randint(-7, -1)
        if tmp not in the_wrong_3 and tmp is not right:
            the_wrong_3.append(tmp)
    return the_wrong_3