import struct
import pathlib
import threading
from datetime import datetime
from .utils.listener import Listener


class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, conn, data_dir):
        super().__init__()
        self.conn = conn
        self.data_dir = data_dir

    def run(self):
        """
        Handles current connection by receiving its data, acquiring the lock,
        writing the user's thought to the appropriate path on disk, and
        finally releasing the lock.
        """
        # Receive current connection's data.
        header = self.conn.receive(struct.calcsize('LLI'))
        user_id, timestamp, thought_size = struct.unpack('LLI', header)
        timestamp = datetime.fromtimestamp(timestamp)
        filename = timestamp.strftime('%Y-%m-%d_%H-%M-%S.txt')
        thought_utf = self.conn.receive(thought_size)
        thought = thought_utf.decode()

        self.lock.acquire()
        try:
            # If the user directory doesn't exist, create it.
            user_data_dir = pathlib.Path(self.data_dir) / str(user_id)
            if not user_data_dir.exists():
                user_data_dir.mkdir(parents=True, exist_ok=True)

            # Write the user's thought to disk.
            path = user_data_dir / filename
            if path.exists():
                thought = f'\n{thought}'
            with path.open(mode='a') as f:
                f.write(thought)

        finally:
            self.conn.close()
            self.lock.release()


def run_server(address, data_dir):
    """Run the server."""
    host, port = address
    with Listener(port, host) as listener:
        try:
            while True:
                conn = listener.accept()
                handler = Handler(conn, data_dir)
                handler.start()
        except KeyboardInterrupt:
            pass
