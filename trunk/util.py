#coding=cp936
import random

def int2hex(number, length):
    s = hex(number)[2:]
    
    return "0"*(length-len(s))+s

def GenTranID():
    a =''
    for i in xrange(32):
        a+=random.choice('0123456789ABCDEF')
    #return binascii.a2b_hex(a)
    return a

def log():
    pass    