#!/usr/bin/env python
#coding=utf-8
import socket, sys, struct, binascii, random

#stun attributes
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
SecondaryAddress = '8050' # Non standard extention

#types for a stun message 
BindRequestMsg               = '0001'
BindResponseMsg              = '0101'
BindErrorResponseMsg         = '0111'
SharedSecretRequestMsg       = '0002'
SharedSecretResponseMsg      = '0102'
SharedSecretErrorResponseMsg = '0112'

MsgAttribute = {}#the attributes which will send to the stun server
stunServerName = "stunserver.org"
stunServerPort = 3478

def createBindRequestMsg(MsgAttribute):
    msg    = ""
    length = 0
    attributeName = MsgAttribute.keys()
    
    for name in attributeName:
        length += (len(MsgAttribute[name]) + 4)
        
    msg += (BindRequestMsg + int2hex(length))
    tranID = generateID()
    msg += tranID
    for name in attributeName:
        msg += name
        attributeValue = MsgAttribute[name]
        msg += int2hex(len(attributeValue))
        msg += attributeValue
        
    msg = binascii.a2b_hex(msg)
    print "message length is %d"%len(msg)
    fp = open("E:\\one.txt", "wb")
    fp.write(msg)
    fp.close()
    
    return msg
    

def int2hex(number):
    #number is a int number
    #return the 2bytes of hex
    s = hex(number)[2:]
    
    return "0"*(4 - len(s))+s
    
def generateID():
    a =''
    for i in xrange(32):
        a+=random.choice('0123456789ABCDEF')
    #return binascii.a2b_hex(a)
    return a
       
if __name__=="__main__":
    print int2hex(5)
    print generateID()
    MsgAttribute[ChangeRequest] = "00000000"
    msg = createBindRequestMsg(MsgAttribute)
    
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cSocket.settimeout(10)
    cSocket.sendto(msg, (stunServerName, stunServerPort))
    print "send to message successful!"
    #print cSocket.getpeername()
    responseMessage = cSocket.recv(512)
    print "receive message!"
    resFp = open("E:\\resOne.txt", "wb")
    resFp.write(responseMessage)
    resFp.close()