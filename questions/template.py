import random

def addition_upto_10():
    """Add a docstring that makes sense for this random generation.
    
    Be sure to return the results in the return format shown
    """
    term_1, term_2, right = generate_question()
    generate_question(term_1, term_2)
    return (term_1, term_2, right, wrong1, wrong2, wrong3)

def generate_question():
    """This will make the question and will spit out a math question.

    Use the conditions of the question being made to generate a question that
    follows the guidelines, make sure if using any division to except all
    ZeroDivisionErrors and just retry with new numbers
    
    All questions involving subtraction should have no negitive numbers, and
    everything involving fractions should have the same denomenator
    
    When sending a fraction send a string in the format:
        'numerator/denomenator'
    And the result should also be in this format, This template might be updated
    to show a better example of this use

    For division, when remainders are desired, return the string:
        'numberRremainder' (no spaces)

    But within the program feel free to pass the remainder into the
    generate_wrong function, since a common error might be a remainder one
    greater, but the correct other number, or one other number more but the
    right remainder.
    """
    return (term_1, term_2, right)

def generate_wrong(term_1, term_2):
    """This will create _10_ wrong answers and pick 3 that do not repeat
    
    wrongs[] will contain many wrong answers, to create a wrong answer use the
    terms given (term_1 and term_2) to create a plausible mistake for example,
    wrongs.append(term_1 + term_2 + 1)
    as if the user added one extra

    Several random answers should be included too, this is just to make sure
    that the smart ones do not find the answer that is between two that are one
    larger and one less than one of the answers. And some operations will have
    more likely wrong answers than others, like subtraction might be mistaken
    for addition, or devision for multiplication. Keep in mind when writing the
    functions that a sign mismatch is common among little kids, along with
    errors when counting (that is why +1 and -1 work for wrong answers
    """
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

