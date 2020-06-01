import pathlib
import struct

from bci.reader import Reader
from bci.protocol.utils.display import display_user, display_snapshot

ROOT = pathlib.Path(__file__).absolute().parent.parent
PROTO_SAMPLE_PATH = ROOT / 'sample.mind.gz'
MAX_SNAPSHOTS_NUM = 100

if __name__ == '__main__':
    reader = Reader(PROTO_SAMPLE_PATH)
    with open(ROOT / 'test_sample.mind', 'wb') as f:
        display_user(reader.user)
        user_data = reader.user.SerializeToString()
        user_size = struct.pack('<I', len(user_data))
        f.write(user_size + user_data)
        counter = 1
        for snapshot in reader:
            print(f'{counter}: ',)
            display_snapshot(snapshot)
            snapshot_data = snapshot.SerializeToString()
            snapshot_size = struct.pack('<I', len(snapshot_data))
            f.write(snapshot_size + snapshot_data)
            counter += 1
            if counter > MAX_SNAPSHOTS_NUM:
                break



