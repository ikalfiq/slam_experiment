class Test:
    def store(num1, num2):
        print(num1)
        print(num2)

if __name__ == '__main__':
    # You need to directly access the method in the class to pass arguments
    a = Test.store(1, 2)
    b = Test.store(3, 4)

    # It seems easier to use classes without using __init__
    # But when programs get larger and more complex, it would be better to handle all the
    # initializations in the __init__ method rather than directly in the methods