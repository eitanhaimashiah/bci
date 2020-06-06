import pytest
import multiprocessing
import time
import requests

from bci.server import run_server
from bci.defaults import DEFAULT_SERVER_ACTUAL_HOST, \
    DEFAULT_SERVER_PORT, OK_STATUS_CODE


_HOST = DEFAULT_SERVER_ACTUAL_HOST
_PORT = DEFAULT_SERVER_PORT
_URL = f'http://{_HOST}:{_PORT}'
_FIELDS = ['pose', 'color_image', 'depth_image', 'feelings']


@pytest.fixture
def get_message():
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_server,
                                      args=(child,))
    process.start()
    parent.recv()
    try:
        def get_message():
            if not parent.poll(1):
                raise TimeoutError()
            return parent.recv()

        yield get_message
    finally:
        process.terminate()
        process.join()


def test_get_config(get_message):
    time.sleep(1)
    config = requests.get(f'{_URL}/config').json()
    assert 'fields' in config
    assert set(config['fields']) == set(_FIELDS)


def test_post_snapshot(get_message, raw_data, raw_data_json):
    time.sleep(1)
    response = requests.post(f'{_URL}/snapshot', raw_data)
    assert response.status_code == OK_STATUS_CODE
    assert get_message() == raw_data_json


def _run_server(pipe):
    def publish(message):
        pipe.send(message)
    pipe.send('read')
    run_server(host=_HOST, port=_PORT, publish=publish)
