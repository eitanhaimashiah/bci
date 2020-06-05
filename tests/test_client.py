import pytest
import flask
import subprocess
import multiprocessing

from bci.defaults import DEFAULT_SERVER_ACTUAL_HOST, DEFAULT_SERVER_PORT
from bci.client import upload_sample

_HOST = DEFAULT_SERVER_ACTUAL_HOST
_PORT = DEFAULT_SERVER_PORT


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


def test_upload_sample(get_message, raw_data_and_path):
    data, path = raw_data_and_path
    upload_sample(path=path,
                  host=_HOST,
                  port=_PORT)
    assert get_message() == data


def test_cli(get_message, raw_data_and_path):
    data, path = raw_data_and_path
    process = subprocess.Popen(
        ['python', '-m', 'bci.client', 'upload-sample',
         '-h', _HOST, '-p', str(_PORT), str(path)],
        stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert b'done' in stdout.lower()
    assert get_message() == data


def test_cli_error(raw_data_and_path):
    data, path = raw_data_and_path
    process = subprocess.Popen(
        ['python', '-m', 'bci.client', 'upload-sample',
         '-h', _HOST, '-p', str(_PORT), str(path)],
        stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert b'error' in stdout.lower()


def _run_server(pipe):
    app = flask.Flask(__name__)

    @app.route('/config', methods=['GET'])
    def get_config():
        return flask.jsonify({
            'fields': ['feelings', 'color_image', 'pose', 'depth_image'],
            'error': None})

    @app.route('/snapshot', methods=['POST'])
    def snapshot():
        pipe.send(flask.request.data)
        return ""

    pipe.send('read')
    app.run(host=_HOST, port=_PORT)
