import pathlib
import struct

from ..reader import Reader
from ..protocol.utils.display import display_user, display_snapshot

ROOT = pathlib.Path(__file__).absolute().parent.parent
SAMPLE_FILE = 'sample.mind.gz'


def create_mini_sample(root=ROOT, sample_file=SAMPLE_FILE, max_snapshots_num=100):
    sample_path = root / sample_file
    mini_sample_path = root / f'mini_{sample_file}'
    reader = Reader(sample_path)
    with open(mini_sample_path, 'wb') as f:
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
            if counter > max_snapshots_num:
                break
