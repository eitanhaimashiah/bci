import socket


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        src_ip, src_port = self.socket.getsockname()
        dst_ip, dst_port = self.socket.getpeername()
        return f'<Connection from {src_ip}:{src_port} to {dst_ip}:{dst_port}>'

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data = b''
        while size > 0:
            chunk = self.socket.recv(size)
            if not chunk:
                raise RuntimeError(
                    'connection was closed before all the data was received'
                )
            data += chunk
            size -= len(chunk)
        return data

    def close(self):
        self.socket.close()
