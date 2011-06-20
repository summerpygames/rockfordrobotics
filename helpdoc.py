def help(operation, difficulty): 

    if operation not in range(1,5):
        raise IOError('operation is 1-4')

    if difficulty not in range(1,3):
        raise IOError('difficulty is 1-2')

    if operation is 1:
        return'''Help - Addition
            
        Using circles as an example, 2 + 2 would be:
         ___       ___           ___       ___      
        /   \\    /   \\  and   /   \\    /   \\    
        \\___/    \\___/        \\___/    \\___/    
            
        If you count the circles, there are 4 alltogether.
        2 on the left and 2 on the right.
        '''

    elif operation is 2 and difficulty is 1:
        return'''Help - Subtraction
        Using circles as an example, 3 - 1 would be:
            ___       ___        ___
           /   \\    /   \\     /   \\
           \\___/    \\___/     \\___/ 
            
        But your getting rid of 1, so you are left with
            ___      ___
           /   \\    /   \\
           \\___/    \\___/
            
        If you count the circles, there were 3, then 1 was taken away, 
        leaving 2 left.
        '''

    elif operation is 2 and difficulty is 1:
        return'''Help - Subtraction (Advanced)
        Using circles as an example, 2 - 5 would be:
             ___      ___
            /   \\    /   \\
            \\___/    \\___/
            
            But your getting rid of 5.
            ___
give 1      /   \\
            \\___/
            
            
give 2     (you have nothing)
            
            
             ___
give 3      /owe\\                         (you owe 1)
            \\___/
            
             ___      ___
give 4      /owe\\    /owe\\                (you owe 2)
            \\___/    \\___/
            
             ___       ___        ___
give 5      /owe\\    /owe\\     /owe\\    (you owe 3)
            \\___/    \\___/     \\___/ 
            
            For every one you owe, it counts as a negative.
            So if 2-5 gets you owing 3, think of it as negative 3 or '-3'
            '''

    elif operation is 3:
        return'''Sorry kid you are on your own'''

    elif operation is 4 and difficulty is 1:
        return'''Sorry kid you are on your own'''
    
    elif operation is 4 and difficulty is 2:
        return'''Sorry kid you are on your own'''
        
