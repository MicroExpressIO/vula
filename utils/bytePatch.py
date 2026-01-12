

class BytePatch():
    def __init__(self, login_name: str, login_pass: str):
        self.username = login_name
        self.password = login_pass

    def getComments(self, qid: str) -> str:
        # request comments by QID
        pass

    def ifQidCommentsExist(self, qid: str) -> bool:
        comms = ""
        comms =  self.getComments(qid)
        if not comms:
            return False
        return True

    def updateComments(self, qid, comments: str) -> bool:
        pass

    def appendComments(self, qid, comments: str) -> bool:
        existComm = self.getComments(qid)
        return self.updateComments(qid, existComm + "\n" + comments)
    
    def createQidComments(self, qid: str, comments: str) -> bool:
        ### input inspection
        
        ### create new or update existed
        if self.ifQidCommentsExist(qid): 
            print("create new")
        else:
            print("update existed")



        
