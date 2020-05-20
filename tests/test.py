import pathlib

from bci.reader import read, Reader
from bci.client import upload_sample
from bci.server import run_server
from bci.protocol.utils.display import display_user, display_snapshot
from bci.parsers import load_parsers, run_parser
from bci.publisher.drivers import find_driver
from bci.protocol.utils.context import Context
from bci.protocol.utils.json_format import json_user, json_snapshot, json_snapshot_metadata

ROOT = pathlib.Path(__file__).absolute().parent.parent
PROTO_SAMPLE_PATH = ROOT / 'sample.mind.gz'
BINARY_SAMPLE_PATH = ROOT / 'sample.mind'
BLOBS_DIR = ROOT / 'blobs'
DATA_DIR = ROOT / 'data'

if __name__ == '__main__':
    # Test Reader
    read(PROTO_SAMPLE_PATH)
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
    # reader = Reader(PROTO_SAMPLE_PATH)
    # print('user:')
    # user = reader.user
    # display_user(user)
    # print(json_user(user))
    # print('-'*10 + '\nsnapshot:')
    # snapshot = next(reader)
    # display_snapshot(snapshot)
    # print(json_snapshot(snapshot, user.user_id, 'root'))

    # Generate `data` directory for implementing API and GUI
    # context = Context(DATA_DIR)
    # reader = Reader(PROTO_SAMPLE_PATH)
    # user = reader.user
    # context.set(user=user)
    # context.save('metadata.json', json_user(user))
    # display_user(user)
    # for snapshot in reader:
    #     context.set(snapshot=snapshot)
    #     context.save('metadata.json', json_snapshot_metadata(snapshot))
    #     parsers = load_parsers()
    #     for topic in parsers.keys():
    #         run_parser(topic, context, snapshot)
    #     display_snapshot(snapshot)
