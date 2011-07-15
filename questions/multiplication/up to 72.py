import random

def multiple(n,d):
    if n % d == 0:
        return True
    else:
        return False

def generate():
    """"""
    term1, term2, right = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right)
    return (term1, term2, right, wrong1, wrong2, wrong3)

def generate_question():
    """This will make a multiplication question to have results equal to or less than 18"""
    a = 0
    while a == 0:
        right = random.randint(2,72)
        for i in range(1,73):
            if multiple(right,i):
                a = 1
                b = i
                break
    term1 = right/b
    term2 = b
    return (term1, term2, right)

def generate_wrong(term1, term2, right):
    wrongs = []
    wrongs.append(right + 1)
    wrongs.append(right - 1)
    wrongs.append(right + 2)
    wrongs.append(right - 2)
    wrongs.append(term1 + term2)
    wrongs.append(abs(term1-term2))
    wrongs.append(random.randint(1, 72))
    wrongs.append(random.randint(1, 72))
    wrongs.append(random.randint(1, 72))
    wrongs.append(random.randint(1, 72))

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
