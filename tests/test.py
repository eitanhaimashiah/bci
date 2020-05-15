import pathlib

from bci.reader import read, Reader
from bci.client import upload_sample
from bci.server import run_server
from bci.protocol.utils.display import display_user, display_snapshot
from bci.parsers import load_parsers
from bci.publisher.drivers import find_driver
from bci.protocol.utils.context import Context
from bci.protocol.utils.json_format import json_user, json_snapshot
from bci.protocol import sample_pb2 as pb


ROOT = pathlib.Path(__file__).absolute().parent.parent
PROTO_SAMPLE_PATH = ROOT / 'sample.mind.gz'
BINARY_SAMPLE_PATH = ROOT / 'sample.mind'
BLOBS_DIR = ROOT / 'blobs'

if __name__ == '__main__':
    # Test Reader
    # read(PROTO_SAMPLE_PATH)
    # read(BINARY_SAMPLE_PATH, format='binary')

    # Test Context and `save_blobs`
    # context = Context(BLOBS_DIR)
    # reader = Reader(PROTO_SAMPLE_PATH)
    # display_user(reader.user)
    # for snapshot in reader:
    #     display_snapshot(snapshot)
    #     context.save_blobs(reader.user, snapshot)

    # Test Client
    # upload_sample(path=PROTO_SAMPLE_PATH)
    # upload_sample(path=BINARY_SAMPLE_PATH, format='binary')

    # Test Server
    # run_server(publish=display_snapshot)

    # Test Parsers
    # parsers = load_parsers()
    # print(parsers.keys())

    # Test Publisher
    # print(find_driver('rabbitmq://127.0.0.1:5672/'))

    # Test json util
    reader = Reader(PROTO_SAMPLE_PATH)
    print('user:')
    user = reader.user
    display_user(user)
    print(json_user(user))
    print('-'*10 + '\nsnapshot:')
    snapshot = next(reader)
    display_snapshot(snapshot)
    print(json_snapshot(snapshot, user.user_id, 'root'))
