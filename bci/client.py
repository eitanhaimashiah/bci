import socket
from datetime import datetime
from .thought import Thought
from .utils.connection import Connection


def upload_thought(address, user, thought):
    """Upload a new thought."""
    sock = socket.socket()
    sock.connect(address)
    conn = Connection(sock)
    try:
        data = Thought(user, datetime.now(), thought)
        conn.send(data.serialize())
    finally:
        conn.close()
    print('done')
