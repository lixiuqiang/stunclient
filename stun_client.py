#!/usr/bin/env python
#coding=utf-8

#iphone-stun.freenet.de:3478
#larry.gloo.net:3478
#stun.xten.net:3478
#stun.sipgate.net:10000


import socket, sys, struct, binascii, random

#stun attributes
"""
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

dictAttrToVal ={'MappedAddress'   : MappedAddress,
                'ResponseAddress' : ResponseAddress,
                'ChangeRequest'   : ChangeRequest,
                'SourceAddress'   : SourceAddress,
                'ChangedAddress'  : ChangedAddress,
                'Username'        : Username,
                'Password'        : Password,
                'MessageIntegrity': MessageIntegrity,
                'ErrorCode'       : ErrorCode,
                'UnknownAttribute': UnknownAttribute,
                'ReflectedFrom'   : ReflectedFrom,
                'XorOnly'         : XorOnly,
                'XorMappedAddress': XorMappedAddress,
                'ServerName'      : ServerName,
                'SecondaryAddress': SecondaryAddress}

dictMsgTypeToVal = {'BindRequestMsg'              :BindRequestMsg,
                    'BindResponseMsg'             :BindResponseMsg,
                    'BindErrorResponseMsg'        :BindErrorResponseMsg,
                    'SharedSecretRequestMsg'      :SharedSecretRequestMsg,
                    'SharedSecretResponseMsg'     :SharedSecretResponseMsg,
                    'SharedSecretErrorResponseMsg':SharedSecretErrorResponseMsg}
           
Blocked              = "Blocked"
OpenInternet         = "Open Internet"
FullCone             = "Full Cone"
SymmetricUDPFirewall = "Symmetric UDP Firewall"
RestricNAT           = "Restric NAT"
RestricPortNAT       = "Restric Port NAT"
SymmetricNAT         = "Symmetric NAT"
"""
import stun

if __name__ == "__main__":
    stun.getNatType()