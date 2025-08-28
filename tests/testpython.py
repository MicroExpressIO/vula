

MAX_SIZE = 1000
class test:
    def __init__(self):
        self.size = 0
        self.data = []
    
    def add(self, value:  int) -> int:
        if self.size >= MAX_SIZE:
            return -1
        self.data.append(value)
        self.size += 1
        return value

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        return self.data[index]

def testlist():
    t = test()
    print(t.add(1))  # Output: 1
    print(t.add(2))  # Output: 2
    print(t.add(3))  # Output: 3
    print(t.add(4))  # Output: 4
    print(t.add(5))

    print(f"list : {t.data}")

    print(f"list[-3:-1]: {t.data[-3:-1]}")  # Output: [3, 4]
    print(f"list[:-3]: {t.data[:-3]}")  # Output: [1, 2]
    print(t.data[0])
    print(t.data[1])
    print(t.data[2])
    print(t.data[3])
    print(t.data[4])
    print(t.data[-1])
    print(t.data[-2])
    print(t.data[-3])

def main():
    testlist()    

if __name__ == "__main__":
    main()
    # print(t.get(0))  # Output: 1