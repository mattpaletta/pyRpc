from uuid import uuid4


class RpcRequest(object):
    """
    RpcRequest

    Represents a request message to be sent out to a host
    with published services. Used by RpcConnection when doing
    calls.
    """

    def __init__(self):
        self._method = ""
        self._args   = []
        self._kwargs = {}
        self._callback = False
        self._async = False

        self._callback_id = uuid4().int

    def __repr__(self):
        return "<%s: %s (#args:%d, #kwargs:%d)>" % (self.__class__.__name__,
                                                      self.method,
                                                      len(self.args),
                                                      len(self.kwargs))

    @property
    def async(self):
        return self._async

    @async.setter
    def async(self, m):
        if not isinstance(m, bool):
            raise TypeError("async value must be True or False")
        self._async = m

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, m):
        if not isinstance(m, str):
            raise TypeError("method value must be a string name")
        self._method = m

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        if not isinstance(args, (list, tuple)):
            raise TypeError("args parameter must be a list or tuple")
        self._args = args

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        if not isinstance(kwargs, dict):
            raise TypeError("kwargs parameter must be a dict")
        self._kwargs = kwargs

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, cbk):

#        if cbk is None:
#            self._callback = None
#            return
#
#        if not isinstance(cbk, str) and not hasattr(cbk, "__call__") :
#            raise TypeError("Callback value must either be a callable, or string name of callable")

        self._callback = cbk

    @property
    def id(self):
        return self._callback_id