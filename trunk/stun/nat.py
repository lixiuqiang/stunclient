#coding=cp936
# Code for NATs and the like. Also includes code for determining local IP
# address (suprisingly tricky, in the presence of STUPID STUPID STUPID
# networking stacks)

from twisted.internet import defer
from twisted.internet.protocol import DatagramProtocol
import random, socket
from twisted.python import log
from defcache import DeferredCache

# from shtoom.interfaces import StunPolicy as IStunPolicy

_Debug = False

class LocalNetworkMulticast(DatagramProtocol, object):

    def __init__(self, *args, **kwargs):
        self.compDef = defer.Deferred()
        self.completed = False
        super(LocalNetworkMulticast,self).__init__(*args, **kwargs)

    def listenMulticast(self):
        from twisted.internet import reactor
        from twisted.internet.error import CannotListenError
        attempt = 0
        port = 11000 + random.randint(0,5000)
        while True:
            try:
                mcast = reactor.listenMulticast(port, self)
                break
            except CannotListenError:
                port = 11000 + random.randint(0,5000)
                attempt += 1
                print "listenmulticast failed, trying", port
        if attempt > 5:
            log.msg("warning: couldn't listen ony mcast port", system='network')
            d, self.compDef = self.compDef, None
            d.callback(None)
        mcast.joinGroup('239.255.255.250', socket.INADDR_ANY)
        self.mcastPort = port

    def blatMCast(self):
        # XXX might need to set an option to make sure we see our own packets
        self.transport.write('ping', ('239.255.255.250', self.mcastPort))
        self.transport.write('ping', ('239.255.255.250', self.mcastPort))
        self.transport.write('ping', ('239.255.255.250', self.mcastPort))

    def datagramReceived(self, dgram, addr):
        if self.completed:
            return
        elif dgram != 'ping':
            return
        else:
            self.completed = True
            d, self.compDef = self.compDef, None
            d.callback(addr[0])

_cachedLocalIP = None
def _cacheLocalIP(res):
    global _cachedLocalIP
    if _Debug: print "caching value", res
    _cachedLocalIP = res
    return res

# If there's a need to clear the cache, call this method (e.g. DHCP client)
def _clearCachedLocalIP():
    _cacheLocalIP(None)

def _getLocalIPAddress():
    # So much pain. Don't even bother with
    # socket.gethostbyname(socket.gethostname()) - the number of ways this
    # is broken is beyond belief.
    from twisted.internet import reactor
    global _cachedLocalIP
    if _cachedLocalIP is not None:
        print "return _cacheLocalIP:%s"%str(_cacheLocalIP)
        return defer.succeed(_cachedLocalIP)
    # first we try a connected udp socket
    if _Debug: print "resolving A.ROOT-SERVERS.NET"
    
    print "resolving A.ROOT-SERVERS.NET"
    d = reactor.resolve('A.ROOT-SERVERS.NET')
    d.addCallbacks(_getLocalIPAddressViaConnectedUDP, _noDNSerrback)
    return d

getLocalIPAddress = DeferredCache(_getLocalIPAddress)

def _noDNSerrback(failure):
    # No global DNS? What the heck, it's possible, I guess.
    if _Debug: print "no DNS, trying multicast"
    return _getLocalIPAddressViaMulticast()

def _getLocalIPAddressViaConnectedUDP(ip):
    from twisted.internet import reactor
    from twisted.internet.protocol import DatagramProtocol
    if _Debug: print "connecting UDP socket to", ip
    
    print "connecting UDP socket to", ip
    prot = DatagramProtocol()
    p = reactor.listenUDP(0, prot)
    res = prot.transport.connect(ip, 7)
    locip = prot.transport.getHost().host
    p.stopListening()
    del prot, p

    if _Debug: print "connected UDP socket says", locip
        
    print "connected UDP socket says", locip
    
    if isBogusAddress(locip):
        # #$#*(&??!@#$!!!
        if _Debug: print "connected UDP socket gives crack, trying mcast instead"
        
        print "connected UDP socket gives crack, trying mcast instead"

        return _getLocalIPAddressViaMulticast()
    else:
        return locip

def _getLocalIPAddressViaMulticast():
    # We listen on a new multicast address (using UPnP group, and
    # a random port) and send out a packet to that address - we get
    # our own packet back and get the address from it.
    from twisted.internet import reactor
    from twisted.internet.interfaces import IReactorMulticast
    try:
        IReactorMulticast(reactor)
    except:
        if _Debug: print "no multicast support in reactor"
        log.msg("warning: no multicast in reactor", system='network')
        return None
    locprot = LocalNetworkMulticast()
    if _Debug: print "listening to multicast"
    locprot.listenMulticast()
    if _Debug: print "sending multicast packets"
    locprot.blatMCast()
    locprot.compDef.addCallback(_cacheLocalIP)
    return locprot.compDef

def isBogusAddress(addr):
    """ 
    Returns true if the given address is bogus, i.e. 0.0.0.0 or
    127.0.0.1. Additional forms of bogus might be added later.
    """
    if addr.startswith('0.') or addr.startswith('127.'):
        return True
    return False

if __name__ == "__main__":
#     from twisted.internet import gtk2reactor
#     gtk2reactor.install()
    from twisted.internet import reactor
    import sys

    log.FileLogObserver.timeFormat = "%H:%M:%S"
    log.startLogging(sys.stdout)

    def cb_gotip(addr):
        print "got local IP address of", addr

    d1 = getLocalIPAddress().addCallback(cb_gotip)
    d1.addCallback(lambda x:reactor.stop())
    reactor.run()
   
