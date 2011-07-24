import random
from math import sqrt

def generate():
    """Subtracting two numbers to a maximum difference of 100."""
    term1, term2, right = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right)
    return (term1, '-', term2, right, wrong1, wrong2, wrong3, 'standard')
    
def generate_question():
    """This is generating the three terms involved in the sum."""
    right = random.choice(range(1,1001))
    term1 = random.choice(range(right,1001))
    term2 = term1 - right
    if term2 > term1:
        term3 = term1
        term1 = term2
        term2 = term3
    term1list = []
    term2list = []
    for i in range(len(str(term1))):
        i += 1
        term1list.append(int(str(term1)[-i]))
    for i in range(len(str(term2))):
        i += 1
        term2list.append(int(str(term2)[-i]))
    term1list.reverse()
    term2list.reverse()
    term1str = ''
    term2str = ''
    for i in range(len(str(term2))):
        if i in range(len(str(right))):
            i += 1
            while term1list[-i] < term2list[-i]:
                if i-1 in range(len(str(right))) and int(str(right)[-i]) is 9:
                    term1list[-i] = 9
                else:
                    term1list[-i] = int(random.choice(range(int(str(right)[-i]),9)))
                term2list[-i] = term1list[-i] - int(str(right)[-i])
                if len(term1list) is 4 and term1list[0] is 1 and term1list[1] is 0 and term1list[2] is 0 and term1list[3] is not 0:
                    term1list.pop(0)
                    term1list[0] = 9
    for i in range(len(term1list)):
        term1str = term1str + str(term1list[i])
    for i in range(len(term2list)):
        term2str = term2str + str(term2list[i])
    term1 = int(term1str)
    term2 = int(term2str)
    return (term1, term2, right)
    
def generate_wrong(term1, term2, right):
    """Giving many wrong answers to choose from."""
    wrongs = []
    wrongs.append(right + 10)
    wrongs.append(abs(right - 10))
    wrongs.append(right + 20)
    wrongs.append(abs(right - 20))
    wrongs.append(30*int(sqrt(right)))
    wrongs.append(right + 100)
    wrongs.append(abs(right - 100))
    wrongs.append(right + 200)
    wrongs.append(abs(right - 200))
    wrongs.append(random.randint(0, 1000))
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