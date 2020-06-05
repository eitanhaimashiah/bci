import pytest
import datetime as dt
import multiprocessing
import signal
import socket
import struct
import subprocess
import threading
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
    config = requests.get(f'{_URL}/config').json()
    assert 'fields' in config
    assert config['fields'] == _FIELDS


def test_post_snapshot(get_message, raw_data, raw_data_json):
    response = requests.post(f'{_URL}/snapshot', raw_data)
    assert response.status_code == OK_STATUS_CODE
    assert get_message() == raw_data_json


# def test_partial_data(data_dir):
#     message = _serialize_thought(_USER_1, _TIMESTAMP_1, _THOUGHT_1)
#     with socket.socket() as connection:
#         time.sleep(0.1) # Wait for server to start listening.
#         connection.connect(_SERVER_ADDRESS)
#         for c in message:
#             connection.sendall(bytes([c]))
#             time.sleep(0.01)
#     thought_path = _get_path(data_dir, _USER_1, _TIMESTAMP_1)
#     assert thought_path.read_text() == _THOUGHT_1
# def test_race_condition(data_dir):
#     timestamp = _TIMESTAMP_1
#     for _ in range(10):
#         timestamp += 1
#         _upload_thought(_USER_1, timestamp, _THOUGHT_1)
#         _upload_thought(_USER_1, timestamp, _THOUGHT_2)
#         thought_path = _get_path(data_dir, _USER_1, timestamp)
#         thoughts = set(thought_path.read_text().splitlines())
#         assert thoughts == {_THOUGHT_1, _THOUGHT_2}
# def test_cli(tmp_path):
#     host, port = _SERVER_ADDRESS
#     process = subprocess.Popen(
#         ['python', '-m', 'bci', 'run_server', f'{host}:{port}', str(tmp_path)],
#         stdout = subprocess.PIPE,
#     )
#     thread = threading.Thread(target=process.communicate)
#     thread.start()
#     time.sleep(0.5)
#     _upload_thought(_USER_1, _TIMESTAMP_1, _THOUGHT_1)
#     _upload_thought(_USER_2, _TIMESTAMP_2, _THOUGHT_2)
#     process.send_signal(signal.SIGINT)
#     thread.join()
#     thought_path_1 = _get_path(tmp_path, _USER_1, _TIMESTAMP_1)
#     thought_path_2 = _get_path(tmp_path, _USER_2, _TIMESTAMP_2)
#     assert thought_path_1.read_text() == _THOUGHT_1
#     assert thought_path_2.read_text() == _THOUGHT_2

def _run_server(pipe):
    pipe.send('read')
    run_server(host=_HOST, port=_PORT, publish=print)
