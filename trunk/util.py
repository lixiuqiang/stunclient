#coding=cp936
import random

def generateID():
    TranID =''
    for i in xrange(32):
        TranID += random.choice('0123456789ABCDEF')
    #return binascii.a2b_hex(a)
    return TranID

def int2hex(number):
    #number is a int number
    #return the 2bytes of hex
    s = hex(number)[2:]
    
    return "0"*(4 - len(s))+s
    

