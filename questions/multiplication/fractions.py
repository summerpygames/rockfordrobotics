import random

def put(num, denom):
    if int(num) > int(denom):
        front = str(int(num)/int(denom))
        num = str(int(num) % int(denom))
        term = front+'and'+num+'/'+denom
    elif int(num) < int(denom):
        term = '0and'+num+'/'+denom
    else:
        term = '1and0/0'
    return term

def generate():
    term1, term2, right, num1, denom1, num2, denom2, num3, denom3 = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right, num1, denom1, num2, denom2, num3, denom3)
    return (term1, '*', term2, right, wrong1, wrong2, wrong3, 'fraction')

def generate_question():
    denom1 = str(random.randint(2,6))
    denom2 = str(random.randint(2,6))
    denom3 = str(int(denom1) * int(denom2))
    num1 = str(random.randint(1,12))
    num2 = str(random.randint(1,12))
    num3 = str(int(num1) * int(num2))
    term1 = put(num1,denom1)
    term2 = put(num2,denom2)
    right = put(num3,denom3)
    return (term1, term2, right, num1, denom1, num2, denom2, num3, denom3)

def generate_wrong(term1, term2, right, num1, denom1, num2, denom2, num3, denom3):
    wrongs = []
    wrongs.append(str((int(num3)+2))+'/'+denom3)
    wrongs.append(str((abs(int(num3)-2)))+'/'+denom3)
    wrongs.append(str((int(num3)+4))+'/'+denom3)
    wrongs.append(str((abs(int(num3)-4)))+'/'+denom3)
    wrongs.append(str((int(num3)+8))+'/'+denom3)
    wrongs.append(str((abs(int(num3)-8)))+'/'+denom3)
    wrongs.append(str((int(num3)+4))+'/'+str(int(denom3)+2))
    wrongs.append(str((abs(int(num3)-4)))+'/'+str(int(denom3)+4))
    wrongs.append(str((int(num3)+4))+'/'+str(abs(int(denom3)-2)))
    wrongs.append(str((abs(int(num3)-4)))+'/'+str(abs(int(denom3)-4)))
    
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
