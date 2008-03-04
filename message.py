#coding = cp936
messageType   = None
messageLength = 0

class message:
    def __init__(self, changeIP, changePort, TranID):
        #params
        #changeIP, changePort are True or False
        self.messageType   = None
        self.messageLength = 0
        self.TranID        = TranID
        changeRequest      = None
        if changeIP and changePort:
            changeRequest = "00000006"
        elif changeIP and (not changePort):
            changeRequest = "00000004"
        elif (not changeIP) and changePort:
            changeRequest = "00000002"
        elif (not changeIP) and (not changePort):
            changeRequest = "00000000"
        self.attributeDict = {}
        
    def setAttribute(type, value):
        pass
    
    