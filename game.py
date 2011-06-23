from random import choice

def main():
    unpack_output =  levelselector()
    operations, difficulty = unpack_output[0], unpack_output[1]
    print "randomly selecting from the choices you made 1 for addition 2 for sub... :"
    if difficulty is 1:
        print "You are going to be doing easy stuff."
    else:
        print "You are going to be doing easy stuff."
    
    print "you are going to anwser a question about:" + str(choice(operations))
    print "you are going to anwser a question about:" + str(choice(operations))
    print "you are going to anwser a question about:" + str(choice(operations))
    print "you are going to anwser a question about:" + str(choice(operations))
    print "you are going to anwser a question about:" + str(choice(operations))
    
    
def levelselector():
    operations = []
    awesome_factor = 0
    if ask_ok("Do you want to work on Addition? "):
        operations.append(1)
        awesome_factor = awesome_factor + 1
    if ask_ok("Do you want to work on Subtraction? "):
        operations.append(2)
        awesome_factor = awesome_factor + 1
    if ask_ok("Work on Multiplication? "):
        operations.append(3)
        awesome_factor = awesome_factor + 1
    if ask_ok("Devision? "):
        operations.append(4)
        awesome_factor = awesome_factor + 1
    if awesome_factor is 4:
        print("WOW! everything!")
    if ask_ok("Do you want to do the hard stuff? "):
        difficulty = 2
    else:
        difficulty = 1
    return (operations, difficulty)
        

def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
    while True:
        
        ok = raw_input(prompt)
        if ok in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
            return True
        if ok in ('n', 'no', 'nop', 'nope', 'N', 'NO', 'NOP', 'NOPE'):
            return False
        retries = retries - 1
        if retries < 0:
                raise IOError('refusenik user')
        print complaint
    
if __name__ == '__main__':
    main()
