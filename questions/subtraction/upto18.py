import random

def generate():
    term1, term2, right = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right)
    return (term1, term2, right, wrong1, wrong2, wrong3)

def generate_question():
    term1 = random.randint(1,18)
    term2 = random.randint(0,term1)
    right = term1 - term2
    return (term1, term2, right)

def generate_wrong(term1, term2, right):
    wrongs = []
    wrongs.append(abs(right+1))
    wrongs.append(abs(right-1))
    wrongs.append(abs(right+2))
    wrongs.append(abs(right-2))
    wrongs.append(abs(right-4))
    wrongs.append(random.randint(1, 18))
    wrongs.append(random.randint(1, 18))
    wrongs.append(random.randint(1, 18))
    wrongs.append(random.randint(1, 18))
    wrongs.append(random.randint(1, 18))
    
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
