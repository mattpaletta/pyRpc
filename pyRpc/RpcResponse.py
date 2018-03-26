class RpcResponse(object):
    """
    RpcResponse

    Represents a response message from a remote call.
    Wraps around the result from the remote call.
    Used by splRpc when replying to a call from RpcConnection.
    """

    def __init__(self, result=None, status=-1, error=None):
        self._status = status
        self._result = result
        self._error  = error

    def __repr__(self):
        return "<%s: status:%d>" % (self.__class__.__name__, self.status)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, v):
        if not isinstance(v, int):
            raise TypeError("status value must be an int")
        self._status = v

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, v):
        self._result = v

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, v):
        self._error = v