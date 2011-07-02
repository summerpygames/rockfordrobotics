import random

def addition_upto_10():
    """Add a docstring that makes sense for this random generation."""
    term_1, term_2, right = generate_question()
    generate_question(term_1, term_2)
    return (term_1, term_2, right, wrong1, wrong2, wrong3)

def generate_question():
    """This will make the question and will spit out a math question."""
    return (term_1, term_2, right)

def generate_wrong(term_1, term_2):
    """This will create _10_ wrong answers and pick 3 that do not repeat"""
    wrongs = []
    wrongs.append('create wrong answer')
    wrongs.append('create wrong answer')
    wrongs.append('create wrong answer')
    wrongs.append('create wrong answer')
    wrongs.append('create wrong answer')
    wrongs.append(random.randint(1, 20))
    wrongs.append(random.randint(1, 20))
    wrongs.append(random.randint(1, 20))
    wrongs.append(random.randint(1, 20))
    wrongs.append(random.randint(1, 20))
    
    the_wrong_3 = []

    for i in range(3):
        tmp = random.choice(wrongs)
        wrongs.remove(tmp)
        if tmp not in the_wrong_3:
            the_wrong_3.append(tmp)

