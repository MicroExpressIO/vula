
def two_sum(nums: list, target):
    nums.sort()
    #nums_len = range(nums)
    #print(f"range: {nums_len}")
    for i in range(0, len(nums) -1) :
        #print(nums[i])
        for j in range(1, len(nums)):
            if nums[i] + nums[j] == target:
                #print(f"{nums[i]}, {nums[j]}")
                return(nums[i], nums[j])
def test_twosum():
    nums = [2, 7, 11, 15]
    target = 18
    ret = two_sum(nums, target)
    print(ret)

def solution(queries):
    ret = []
    q = []
    steps = len(queries) 
    print(f"len: {len(queries)}, steps: {steps}")
    for i in range(0, steps):
        if queries[i][0] == "ADD":
            ret.append("")
            q.append(queries[i][1])
        if queries[i][0] == "EXISTS":
            if queries[i][1] in q:
                ret.append("true")
            else:
                ret.append("false")
        #print(f"i: {i}, ret: {ret}, q: {q}")
    return ret   

def test_solution():
    myqueries = [["ADD","1"], 
                    ["ADD","2"], 
                    ["ADD","5"], 
                    ["ADD","2"], 
                    ["EXISTS","2"], 
                    ["EXISTS","5"], 
                    ["EXISTS","1"], 
                    ["EXISTS","4"], 
                    ["EXISTS","3"], 
                    ["EXISTS","0"]]
    ret = solution(myqueries)
    print(ret)

def longestConsecutive(nums: list[int]) -> int:
#def longestConsecutive(nums: list) -> int:
 
    if not nums:
        return 0
    max_len = 0
    num_set = set(nums)

    for n in nums:
        #if (n - 1) not in num_set:
        curr_num = n
        curr_len = 1
        while (curr_num + 1) in num_set:
            curr_num += 1
            curr_len += 1
        max_len = max(max_len, curr_len)

    return max_len


def testLongestCon():
    #mynums = [100, 4, 200, 1, 3, 2]
    #mynums = [3, 100, 4, 200, 1, 2]
    mynums = [0]

    mylen = longestConsecutive(mynums)
    print(f" loginest consecutive sequece lenght: {mylen}")

def longestSubStr(s: str) -> int:
    maxlen = 0
    left = 0


def main():
    #test_twosum()
    #test_solution()
    #testLongestCon()

if __name__ == '__main__':
    main()

    