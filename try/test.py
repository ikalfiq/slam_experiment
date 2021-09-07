class Test:
    def __init__(self, val1, val2):
        self.values = ValueStore(val1, val2)

    
if __name__ == '__main__':
    a = Test(1,2)
    print(a.values)