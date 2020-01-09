import socket
import struct


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

    def send_message(self, message):
        message_size = struct.pack('<I', len(message))
        if isinstance(message, str):
            message = message.encode()
        self.send(message_size + message)

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

    def receive_message(self):
        message_size = self.receive(struct.calcsize('<I'))
        message_size = struct.unpack('<I', message_size)[0]
        message_utf = self.receive(message_size)
        return message_utf.decode()

    def close(self):
        self.socket.close()
