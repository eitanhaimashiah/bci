import pathlib

from bci.reader import read, Reader
from bci.client import upload_sample
from bci.server import run_server
from bci.protocol.utils.display import display_user, display_snapshot
from bci.parsers import load_parsers, parse
from bci.publisher import Publisher
from bci.protocol.utils.context import Context
from bci.protocol.utils.to_dict import user_to_dict, snapshot_to_dict
from bci.saver.drivers import find_driver

ROOT = pathlib.Path(__file__).absolute().parent.parent
PROTO_TEST_SAMPLE_PATH = ROOT / 'mini_sample.mind'
PROTO_SAMPLE_PATH = ROOT / 'sample.mind.gz'
BINARY_SAMPLE_PATH = ROOT / 'sample.mind'
BLOBS_DIR = ROOT / 'blobs'
DATA_DIR = ROOT / 'data'


def subscribe_exchange(field):
    publisher = Publisher(is_subscriber=True)
    def consume_callback(channel, method, properties, body): print(body)
    publisher.subscribe(exchange=field,
                        routing_key=f'{field}.result',
                        queue='saver',
                        callback=consume_callback)


if __name__ == '__main__':
    # Test Reader
    read(PROTO_TEST_SAMPLE_PATH)
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
    # run_server(publish=print)

    # Test to_dict util
    # reader = Reader(PROTO_SAMPLE_PATH)
    # print('user:')
    # user = reader.user
    # display_user(user)
    # print(user_to_dict(user))
    # print('-'*10 + '\nsnapshot:')
    # snapshot = next(reader)
    # display_snapshot(snapshot)
    # print(snapshot_to_dict(snapshot))

    # Generate `data` directory for implementing API and GUI
    # context = Context(DATA_DIR)
    # reader = Reader(PROTO_SAMPLE_PATH)
    # user = reader.user
    # context.set(user=user)
    # context.save('metadata.json', user_to_dict(user))
    # display_user(user)
    # for snapshot in reader:
    #     context.set(snapshot=snapshot)
    #     context.save('metadata.json', json_snapshot_metadata(snapshot)) # TODO replace `json_snapshot_metadata` with the proper function
    #     parsers = load_parsers()
    #     for topic in parsers.keys():
    #         run_parser(topic, context, snapshot)
    #     display_snapshot(snapshot)

    # Test Parsers
    subscribe_exchange('pose')
    subscribe_exchange('color_image')
    subscribe_exchange('depth_image')
    subscribe_exchange('feelings')

    # Test Saver's `find_driver`
    # print(find_driver('postgresql'))