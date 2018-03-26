from threading import Thread, current_thread

import zmq

from client import logger
from RpcRequest import RpcRequest
from constants import TEMPDIR
from RpcResponse import RpcResponse


class RpcConnection(object):
    """
    RpcConnection

    For making remote calls to published services in another
    application (or even the same application). Uses multiple
    worker threads to send out calls and process their
    return values.

    Usage:
        def processResponse(rpcResponse):
            print rpcResponse.result

        rpc = PyRpc.RpcConnection("com.myCompany.MyApplication")  # any useful name
        rpc.call("myFunction", callback=processResponse, args=(1, "a"), kwargs={'flag':True, 'option':"blarg"})
    """

    def __init__(self, name, tcpaddr=None, context=None, workers=1):

        self._context = context or zmq.Context.instance()

        if tcpaddr:
            self._address = "tcp://%s" % tcpaddr
        else:
            self._address = "ipc://%s/%s.ipc" % (TEMPDIR, name)

        self._work_address = "inproc://workRequest"

        self._async_sender = self._context.socket(zmq.PUSH)
        self._async_sender.bind(self._work_address)

        self._main_sender = None

        self.exit_request = False
        self._callbacks = {}

        for i in range(max(int(workers), 1)):
            t = Thread(target=self._worker_routine,
                        args=(self._context, self._address, self._work_address))
            t.daemon = True
            t.start()

    def __del__(self):
        logger.debug("closing connection")
        self.close()

    def close(self):
        """
        close()

        Close the client connection
        """
        self.exit_request = True

    def availableServices(self):
        """
        availableServices() -> RpcResponse

        Asks the remote server to tell us what services
        are published.
        Returns an RpcResponse object
        """
        return self.call("__services__")

    def call(self, method, callback=None, async=False, args=[], kwargs={}):
        """
        call(str method, object callback=None, bool async=False, list args=[], dict kwargs={})

        Make a remote call to the given service name, with an optional callback
        and arguments to be used.
        Can be run either blocking or asynchronously.

        By default, this method blocks until a response is received.
        If async=True, returns immediately with an empty RpcResponse. If a callback
        was provided, it will be executed when the remote call returns a result.
        """

        req = RpcRequest()
        req.method = method
        req.args   = args
        req.kwargs = kwargs
        req.async  = async

        if async or callback:
            if callback:
                req.callback = True
                self._callbacks[req.id] = callback
            else:
                logger.debug("Setting request to async, with no callback")

        logger.debug("Sending a RPC call to method: %s" % method)

        if async or callback:
            # push the request down to the workers
            self._async_sender.send_pyobj(req)
            return RpcResponse(None, 0, None)

        # otherwise, we are running this as a blocking call
        if self._main_sender is None:
            logger.debug("Making connection to RPC server at: %s" % self._address)
            self._main_sender = self._context.socket(zmq.REQ)
            self._main_sender.connect(self._address)

        self._main_sender.send_pyobj(req)
        resp = self._main_sender.recv_pyobj()

        logger.debug("Got reply to method %s: %s" % (method, resp))

        return resp

    def _worker_routine(self, context, remote_address, work_address):
        """
        Worker loop for processing rpc calls.
        """
        logger.debug("Starting local worker thread: %s" % current_thread().name)

        receiver = context.socket(zmq.PULL)
        receiver.connect(work_address)

        logger.debug("Making connection to RPC server at: %s" % remote_address)
        remote = context.socket(zmq.REQ)
        remote.connect(remote_address)

        poller = zmq.Poller()
        poller.register(receiver, zmq.POLLIN)

        while not self.exit_request:

            socks = dict(poller.poll(500))
            if socks.get(receiver, None) == zmq.POLLIN:
                msg = receiver.recv_pyobj()

                cbk = self._callbacks.pop(msg.id, None)

                logger.debug("(%s) Forwarding a RPC call to method: %s" % (current_thread().name, msg.method))
                remote.send_pyobj(msg)
                resp = remote.recv_pyobj()

                if cbk:
                    logger.debug("Response received from server. Running callback.")
                    cbk(resp)