from p2p import PeerConnection

class Contact(object):
    """ Encapsulation for remote contact

    This class contains information on a single remote contact
    """
    def __init__(self, id, ipAddress, port, networkProtocol, firstComm=0):
        self.id = id
        self.address = ipAddress
        self.port = port
        self._peerConnection = PeerConnection(ipAddress, port)
        self.commTime = firstComm

    def __eq__(self, other):
        if isinstance(other, Contact):
            return self.id == other.id
        elif isinstance(other, str):
            return self.id == other
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Contact):
            return self.id != other.id
        elif isinstance(other, str):
            return self.id != other
        else:
            return True

    def __str__(self):
        return '<%s.%s object; IP address: %s, Port: %d>' % (self.__module__, self.__class__.__name__, self.address, self.port)

    def __getattr__(self, name):
        """ This override allows the host node to call a method of the remote
        node (i.e. this contact) as if it was a local function.

        For instance, if C{remoteNode} is a instance of C{Contact}, the
        following will result in C{remoteNode}'s C{test()} method to be
        called with argument C{123}::
         remoteNode.test(123)

        Such a RPC method call will return a Deferred, which will callback
        when the contact responds with the result (or an error occurs).
        This happens via this contact's C{_networkProtocol} object (i.e. the
        host Node's C{_protocol} object).
        """
        def _send():
            return self._networkProtocol.sendRPC(self, name, args, **kwargs)
        return _sendRPC