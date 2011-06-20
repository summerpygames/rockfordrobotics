from random import choice

def main():
    operations, difficulty = levelselector()
    print "randomly selecting from the choices you made 1 for addition 2 for sub...:" + str(choice(operations))
    print "randomly selecting from the choices you made 1 for addition 2 for sub...:" + str(choice(operations))
    print "randomly selecting from the choices you made 1 for addition 2 for sub...:" + str(choice(operations))
    print "randomly selecting from the choices you made 1 for addition 2 for sub...:" + str(choice(operations))
    print "randomly selecting from the choices you made 1 for addition 2 for sub...:" + str(choice(operations))
    print "randomly selecting from the choices you made 1 for addition 2 for sub...:" + str(choice(operations))
    
def levelselector():
    operations = []
    awesome_factor = 0
    if ask_ok("Do you want to work on Addition?"):
        operations.append(1)
        awesome_factor = awesome_factor + 1
    if ask_ok("Do you want to work on Subtraction?"):
        operations.append(2)
        awesome_factor = awesome_factor + 1
    if ask_ok("Work on Multiplication?"):
        operations.append(3)
        awesome_factor = awesome_factor + 1
    if ask_ok("Devision?"):
        operations.append(4)
        awesome_factor = awesome_factor + 1
    if awesome_factor is 4:
        print("WOW! everything!")
    if ask_ok("Do you want to do the hard stuff?"):
        difficulty = 2
    else:
        difficulty = 1
    return (operations, difficulty)
        

def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
    while True:
        ok = raw_input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise IOError('refusenik user')
        print complaint
    
if __name__ == '__main__':
    main()