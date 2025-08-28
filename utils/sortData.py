
import re

class SortData:
    def __init__(self):
        self.test = 1
    
    def findPattern(self, src: str, dstPattern: str) ->list:
        
        ret=re.findall(dstPattern, src, re.I)
        #ret=re.search(dstPattern, src)
        return ret

    
def testfindPattern():
    testStr="6000133-Debian Security Update for libx11 (DLA 3602-1)"
    #dla_pattern = re.compile(r'\b((DLA)\s+(\d{4,})-(\d{1,2}))\b')
    #dla_pattern = re.compile(r'\b(DLA)\s+(\d{4,})-(\d{1,2})\b')
    dla_pattern = re.compile(r'\b(DLA)\s(\d{4})-(\d{1})\b')
    
    dla = r"DLA 3602-1"

    sortdata = SortData()
    #ret=sortdata.findPattern(testStr, dla_pattern)
    #ret=sortdata.findPattern(testStr, dla_pattern)
    ret = dla_pattern.search(testStr)
    #print(f"ret: {ret}")
    print(f"ret: {ret.group(0)}")

def main():
    testfindPattern()

if __name__ == '__main__':
     main()    