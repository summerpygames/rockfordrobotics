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
    term1, term2, right, num1, num2, denom = generate_question()
    wrong1, wrong2, wrong3 = generate_wrong(term1, term2, right, num1, num2, denom)
    return (term1, term2, right, wrong1, wrong2, wrong3)

def generate_question():
    denom = random.randint(2,4)
    num1 = random.randint(denom,12)
    num2 = random.randint(denom,12)
    num3 = num1+num2
    term1 = put(str(num1),str(denom))
    term2 = put(str(num2),str(denom))
    right = put(str(num3),str(denom))
    return (term1, term2, right, num1, num2, denom)

def generate_wrong(term1, term2, right, num1, num2, denom):
    wrongs = []
    wrongs.append(str(abs(num1+num2-1))+"/"+str(denom))
    wrongs.append(str(num1+num2+1)+"/"+str(denom))
    wrongs.append(str(abs(num1+num2-2))+"/"+str(denom))
    wrongs.append(str(num1+num2+2)+"/"+str(denom))
    wrongs.append(str(num1+num2+3)+"/"+str(denom))
    wrongs.append(str(random.randint(1, 24))+"/"+str(denom))
    wrongs.append(str(random.randint(1, 24))+"/"+str(denom))
    wrongs.append(str(random.randint(1, 24))+"/"+str(denom))
    wrongs.append(str(random.randint(1, 24))+"/"+str(denom))
    wrongs.append(str(random.randint(1, 24))+"/"+str(denom))
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