import gameplay
import help s

def play():
    print "\n\n\n\n\n\n\n", p1, symbol, p2, "\n\n\n\n\n"
    #what is your answer?
    user_a=input("your answer: ")
    if user_a=="":
        print "Incorrect. It was ", a
        win=0
    if user_a==a:
        print "Correct"
        win=1
        global points
        points+=10
    elif str(user_a)==str(help):
        if n==1:

        win=0
    else:
        print "Incorrect. It was ", a
        win=0
    #return win so the program knows you got the question right
    return win
def q(n,l):
    #start off with none correct or asked
    correct=0
    asked=0
    #user_b is for racking up more points by repeating the same level
    user_b=2
    while user_b!=1:
        while correct < 6: #after 10 Qs answered, if you failed you repeat another 10 in the same level
            #ask 10 questions
            for i in range(10):
                if question(n,l)==1:
                    correct+=1
                    asked+=1
                    print "You have gotten ", correct, " correct of ", asked
                    #pause. It won't be in the real game.
                    raw_input("Press enter to continue")
                #after answering ten questions and failing, reset correct and asked
            if correct < 6:
                asked=0
                correct=0
        print "Congratulations! You beat stage ", n, " level ", l, "!\n\n\n\n\n\n\n\n\n\n" 
        print "You now have ", points, " points"
        user_b=input("Enter 1 to continue or enter 2 to repeat this level.\n")        
def play():
    '''Document your code, start with a capitol, and end with a period.
    
        then say more and more down here
    '''
    
    print "During gameplay you can enter help instead of the answer for help getting the answer (it counts as incorrect)."
    #this is just to cycle through the stages and levels in order
    for n in range(4):
        for l in range(2):
            q(n+1,l+1)
