#coding=cp936
#实现stun协议的一些内容
import util
import binascii, random, socket, time

BindRequestMsg               = '0001'
BindResponseMsg              = '0101'
BindErrorResponseMsg         = '0111'
SharedSecretRequestMsg       = '0002'
SharedSecretResponseMsg      = '0102'
SharedSecretErrorResponseMsg = '0112'

MappedAddress    = '0001'
ResponseAddress  = '0002'
ChangeRequest    = '0003'
SourceAddress    = '0004'
ChangedAddress   = '0005'
Username         = '0006'
Password         = '0007'
MessageIntegrity = '0008'
ErrorCode        = '0009'
UnknownAttribute = '000A'
ReflectedFrom    = '000B'
XorOnly          = '0021'
XorMappedAddress = '8020'
ServerName       = '8022'
SecondaryAddress = '8050'


SimpleBindRequestMsgLength   = 8

serverName = "stunserver.org"
serverPort = 3478

secondName = None#stun服务器的第二个地址，用于再次发送test1型消息
secondPort = None


stunMsgHdr = {"msgType":None, "msgLength":None, "id":None}

stunAtrChangeRequest = None

messageID = [util.GenTranID(), util.GenTranID(), 
             util.GenTranID(), util.GenTranID()]

class responseMessage:
    #msgType, msgLength, attributeDict
    #attributeDict = {attributeType1:value1,......}
    def __init__(self):
        self.msgType       = None
        self.msgLength     = None
        self.msgTranID     = None
        self.attributeDict = {}
    
    def setType(self, msgType):
        self.msgType = msgType
        
    def setLength(self, msgLength):
        self.msgLength = msgLength
        
    def setTranID(self, msgTranID):
        self.msgTranID = msgTranID
        
    def setAttribute(self, attributeType, value):
        self.attributeDict[attributeType] = value

def builtRequestMsg(*params):
    #params = (changeIP, changePort, id)
    #构造bindrequest消息, return msg
    (changeIP, changePort, id) = params
    changeRequestFlag = (changeIP and 4 or 0)|(changePort and 2 or 0)
    changeRequestFlag = util.int2hex(changeRequestFlag, 8)
    
    msg  = binascii.a2b_hex(BindRequestMsg)#msg type
    msg += binascii.a2b_hex(util.int2hex(SimpleBindRequestMsgLength, 4))#msg length
    msg += binascii.a2b_hex(id)
    msg += binascii.a2b_hex(ChangeRequest)#attribute type
    msg += binascii.a2b_hex("0004")#attribute value length
    msg += binascii.a2b_hex(changeRequestFlag)
    
    fp = open(id+".txt", "wb")
    fp.write(msg)
    fp.close()
    
    
    return msg

def stunSendTest(*params):
    #params = (socket, serverName, serverPort, msg)
    #return the length of the msg which has been sended
    (sock, serverName, serverPort, msg) = params
    length = sock.sendto(msg, (serverName, serverPort)) 
    print "send %d bytes msg to server:%s, port:%d"%(length, serverName, serverPort)
    
    return length

def stunParserMsg(*params):
    #params = (responseMsg)
    #解析返回的消息, return a message class
    (msg,) = params
    resMsg = responseMessage()
    
    start = 0
    
    msgType   = binascii.b2a_hex(msg[start:start+2])
    resMsg.setType(msgType)
    start += 2
    print "msgType is %s"%msgType
    
    msgLength = int(binascii.b2a_hex(msg[start:start+2]), 16)
    resMsg.setLength(msgLength)
    start += 2
    print "msgLength is %d"%msgLength
    
    msgTranID = binascii.b2a_hex(msg[start:start+16])
    resMsg.setTranID(msgTranID)
    start += 16
    print "msgTranID is %s"%(msgTranID)
    fp = open(msgTranID+"_res.txt", "wb")#
    fp.write(msg)#
    fp.close()#
    
    while msgLength > 0:
        attributeType = binascii.b2a_hex(msg[start:start+2])
        start += 2
        msgLength -= 2
        print "attributeType is %s"%attributeType
        
        attributeLength = int(binascii.b2a_hex(msg[start:start+2]))
        start += 2
        msgLength -= 2
        print "attibuteLength is %d"%attributeLength
        
        value = msg[start:start+attributeLength]
        start += attributeLength
        msgLength -= attributeLength
        print "value is %s"%binascii.b2a_hex(value)
        
        resMsg.setAttribute(attributeType, value)
    
    return resMsg    

def getNatType():
    #return (natType, external IP, external port)
    #do test1, changeIP = False, changePort = False
    test1   = False#表示第几个测试的成功与否
    test1_1 = False
    test2   = False
    test3   = False
    
    localPort1 = random.randint(30000, 50000)
    localPort2 = localPort1 + 1
    
    sock1      = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock1.settimeout(20)
    sock1.bind(("", localPort1)) 
    
    sock2      = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock2.settimeout(20)
    sock2.bind(("", localPort2))
    
    """
    send test 1
    """
    changeIP   = False
    changePort = False
    id         = messageID[1]
    msg1 = builtRequestMsg(changeIP, changePort, id)
    stunSendTest(sock1, serverName, serverPort, msg1)
    #开始接受消息
    """
    response1 = sock1.recv(512)
    responseMessageOne = stunParserMsg(response1)
    #TODO do something to store the response Message's information
    """
    """
    send test 2
    """
    changeIP   = True
    changePort = False
    id         = messageID[2]
    msg2       = builtRequestMsg(changeIP, changePort, id)
    stunSendTest(sock1, serverName, serverPort, msg2)
    #接受消息
    """
    response2 = sock1.recv(512)
    responseMessageTwo = stunParserMsg(response2)
    #TODO do something to store the response message
    """
    
    

fp = open("response_one.txt", "rb")
content = fp.read()
stunParserMsg(content)
fp.close()