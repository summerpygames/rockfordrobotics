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
    
if __name__ == '__main__':
