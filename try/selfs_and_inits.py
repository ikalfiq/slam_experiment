class Test:
    # When creating an instance of the class, __init__ will handle all of the initializations
    # Do note that __init__ MUST contain at least one argument (typically named as self)
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    # When defining another method within the class, you must include the 'self' argument
    # else you will get an error related to taking arguments 
    def add(self):
        print(self.num1 + self.num2)

if __name__ == '__main__':
    # Creating an instance of the class 'test', while also passing the arguments
    # Basically the 'self' argument will be substituted with the name of the constructor
    a = Test(1, 2)

    '''
    # The constructor will share the smae attributes as defined in __init__ 
    print(a.num1)
    print(a.num2)

    # You can create another instance of the same class with a different constructor name
    b = Test(3,4)

    # The new constructor will then take the attributes belonging to self in __Init__
    print(b.num1)
    print(b.num2)
    
    # How is this different from creating instances without the __init__ method?
    '''