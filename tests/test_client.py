import flask
import pytest
import multiprocessing
import subprocess
from bci.client import upload_sample
from bci.utils.snaphosts import create_stream

_HOST = 'localhost'
_PORT = 8000


@pytest.fixture
def server_pipe():
    parent, child = multiprocessing.Pipe()

    app = flask.Flask(__name__)

    @app.route('/snapshot', methods=['POST'])
    def snapshot():
        child.send(flask.request.data)
        return ""

    process = multiprocessing.Process(
                    target=_run_server,
                    args=(child, app))

    process.start()
    parent.recv()
    try:
        yield parent

    finally:
        process.terminate()
        process.join()


def test_upload_sample(server_pipe, tmp_path, user, snapshot):
    data = create_stream(user, [snapshot]).read()
    path = tmp_path / 'snapshot.raw'
    path.write_bytes(data)
    upload_sample(_HOST, _PORT, str(path))
    assert server_pipe.recv() == data


def test_client_cli(server_pipe, tmp_path, user, snapshot):
    data = create_stream(user, [snapshot]).read()
    path = tmp_path / 'snapshot.raw'
    path.write_bytes(data)

    process = subprocess.Popen(
        ['python', '-m', 'bubbles.client', 'upload-sample',
         '-h', _HOST, '-p', str(_PORT), str(path)]
    )

    process.communicate()

    assert server_pipe.recv() == data


def _run_server(pipe, app):
    pipe.send('read')
    app.run(host=_HOST, port=_PORT)
