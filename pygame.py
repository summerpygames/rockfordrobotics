def main():
    user_c=input("Enter 1 to start or type 'exit' to leave\n")

    if user_c=="exit":
        exit()
    #this is a way to skip to a stage and level
    elif user_c!=1:
        user_n=input("select stage: ")
        user_l=input("select level: ")
        q(user_n,user_l)
    else:
        play()
    user_c=input("\n\n\n\n\n\n\n\n\n\n\n\nEnter 1 to start\n")
    
def levelselector():
    operations = []
    awesome_factor = 0
    if ask_ok("Do you want to work on Addition?"):
        operations.append(1)
        awesome_factor = awesome_factor + 1
    if ask_ok("Do you want to work on Subtraction?")
        operations.append(2)
        awesome_factor = awesome_factor + 1
    if ask_ok("Work on Multiplication?")
        operations.append(3)
        awesome_factor = awesome_factor + 1
    if ask_ok("Devision?")
        operations.append(4)
        awesome_factor = awesome_factor + 1
    if awesome_factor 
        

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
