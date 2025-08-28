"""
with open("mock_qualys_lkb.csv", "r") as file:
	lines = file.readlines()

for l in lines:
	print (l)
for l in reversed(lines):
	print (l[::-1])

"""
"""
    request: CreateDocumentBlockChildrenRequest = CreateDocumentBlockChildrenRequest.builder() \
        .document_id("XeuVw1pWiifKCQkzzkTcNosKnOh") \
        .document_revision_id(-1) \
        .block_id("XeuVw1pWiifKCQkzzkTcNosKnOh") \
        .text(body_content) \
        .build()
"""


def solution(a):
    #ret = []
    retIndex = -1
    retIndex2 = -1
    minSum = 0
    if len(a) == 1:
        return a[0]
        
    for z in range(len(a)):
        minSum += abs(a[0] - a[z])
        retIndex = 0
        
    for i in range(1, len(a)):
        curSum = 0
        for x in a:
            curSum += abs(x-a[i])
        print(f"curSum: {curSum}, minSum: {minSum}, a[i]: {a[i]}")
        if curSum < minSum :
            minSum = curSum
            retIndex = i
            retIndex2 = -1
            #ret.clear
            #ret.append(a[i])
            print(f"retIndex: {retIndex}")
        elif curSum == minSum:
            #ret.append(a[i])
            retIndex2 = i
            print(f"retIndex2: {retIndex2}")
    #if retIndex2 != -1:
    #    return a[retIndex], a[retIndex2]
    #else:
    return a[retIndex]

def solution2(a):
    indexOfMinimum = -1
    minimalSum = float('inf')
    
    if len(a) == 1:
        return a[0]
        
    for x in a:
        minimalSum += abs(x-a[0])
        indexOfMinimum = 0
        
    for i in range(1, len(a)):
        curSum = 0
        for x in a:
            curSum += abs(x - a[i])

        print(f"curSum: {curSum}, minSum: {minimalSum}, a[i]: {a[i]}")

        if curSum < minimalSum:
            minimalSum = curSum
            indexOfMinimum = i

    return a[indexOfMinimum]

def main():
    a = [2, 3]
    #a = [-10, -10, -10, -10, -10, -9, -9, -9, -8, -8, -7, -6, -5, -4, -3, -2, -1, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    print(f"Input: {a}")
    
    result = solution2(a)
    print(f"Output: {result}")


if __name__ == "__main__":
    main()