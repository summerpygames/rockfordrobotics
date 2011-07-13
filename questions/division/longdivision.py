import random
import math

def denote(num, rem):
    return str(num)+'R'+str(rem)

def generate():
    term1, term2, right, num, rem = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right, num, rem)
    return (term1, term2, right, wrong1, wrong2, wrong3)

def generate_question():
    term1 = int(random.randint(1,1000))
    term2 = int(random.randint(1,1000))
    num = int(term1/term2)
    rem = int(term1 % term2)
    right = denote(num, rem)
    return (term1, term2, right, num, rem)

def generate_wrong(term1, term2, right, num, rem):
    wrongs = []
    wrongs.append(denote(num+10,rem))
    wrongs.append(denote(num+20,abs(rem-1)))
    wrongs.append(denote(abs(num-20),abs(rem-(term2/2))))
    wrongs.append(denote(num,abs(rem-term2)))
    wrongs.append(denote(random.randint(abs(num-10),num+10),random.randint(0,term2)))
    wrongs.append(denote(random.randint(abs(num-10),num+10),random.randint(0,term2)))
    wrongs.append(denote(random.randint(abs(num-10),num+10),random.randint(0,term2)))
    wrongs.append(denote(random.randint(abs(num-10),num+10),random.randint(0,term2)))
    wrongs.append(denote(random.randint(abs(num-10),num+10),random.randint(0,term2)))
    wrongs.append(denote(random.randint(abs(num-10),num+10),random.randint(0,term2)))
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
