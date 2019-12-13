from .connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self._server = None

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'(port={self.port}, ' \
               f'host={self.host!r}, ' \
               f'backlog={self.backlog}, ' \
               f'reuseaddr={self.reuseaddr})'

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()

    def start(self):
        self._server = socket.socket()
        if self.reuseaddr:
            self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(self.backlog)

    def stop(self):
        self._server.close()

    def accept(self):
        client, _ = self._server.accept()
        return Connection(client)
