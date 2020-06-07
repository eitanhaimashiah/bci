import pytest
import subprocess
import datetime as dt

from bci.saver import Saver

_DB_URL = 'postgresql://test:pass@127.0.0.1:3333'
_TOPICS = ['pose', 'color_image', 'depth_image', 'feelings']
_ENDPOINT_TOPIC = [
    ('users', None),
    ('user', None),
    ('snapshots', None),
    ('snapshot', None),
    ('result', 'pose'),
    ('result', 'color_image'),
    ('result', 'depth_image'),
    ('result', 'feelings')
]

s = None


@pytest.fixture
def saver():
    global s
    if not s:
        s = Saver(_DB_URL)
    return s


@pytest.mark.parametrize('topic', _TOPICS)
def test_save(topic, parser_result_json, saver, capsys):
    saver.save(topic=topic, data=parser_result_json)
    stdout, stderr = capsys.readouterr()
    assert stdout == stderr == ''


@pytest.mark.parametrize('endpoint, topic', _ENDPOINT_TOPIC)
def test_get(endpoint, topic, parser_result, saver):
    user_dict = parser_result['user']
    snapshot_dict = parser_result['snapshot']
    result_dict = parser_result['result']
    user_dict['user_id'] = int(user_dict['user_id'])
    user_dict['birthday'] = dt.datetime.fromtimestamp(
        int(user_dict['birthday']))
    snapshot_dict['datetime'] = dt.datetime.fromtimestamp(
        int(snapshot_dict['datetime']) / 1000)
    snapshot_dict['snapshot_id'] = 1
    user_id = user_dict['user_id']
    snapshot_id = snapshot_dict['snapshot_id']
    if endpoint == 'users':
        result = saver.get(endpoint)
        expected_result = [{
            'user_id': user_id,
            'username': user_dict['username']
        }]
    elif endpoint == 'user':
        result = saver.get(endpoint,
                           user_id=user_id,
                           str_dates=False)
        expected_result = user_dict
    elif endpoint == 'snapshots':
        result = saver.get(endpoint,
                           user_id=user_id,
                           str_dates=False)
        expected_result = [snapshot_dict]
    elif endpoint == 'snapshot':
        result = saver.get(endpoint,
                           user_id=user_id,
                           snapshot_id=snapshot_id,
                           str_dates=False)
        expected_result = snapshot_dict
        expected_result['user_id'] = user_id
        expected_result['results'] = _TOPICS
    elif endpoint == 'result':
        result = saver.get(endpoint,
                           result_name=topic,
                           snapshot_id=snapshot_id)
        if topic == 'pose':
            trans_dict = result_dict['translation']
            rot_dict = result_dict['rotation']
            expected_result = {
                'snapshot_id': snapshot_id,
                'translation_x': trans_dict['x'],
                'translation_y': trans_dict['y'],
                'translation_z': trans_dict['z'],
                'rotation_x': rot_dict['x'],
                'rotation_y': rot_dict['y'],
                'rotation_z': rot_dict['z'],
                'rotation_w': rot_dict['w'],
            }
        elif topic == 'color_image' \
                or topic == 'depth_image' \
                or topic == 'feelings':
            expected_result = result_dict
            expected_result['snapshot_id'] = snapshot_id
        else:
            raise ValueError(f'unknown topic: {topic}')

    else:
        raise ValueError(f'unknown endpoint: {endpoint}')
    saver.close()
    assert result == expected_result


@pytest.mark.parametrize('topic', _TOPICS)
def test_cli(topic, parser_result_json_path):
    process = subprocess.Popen(
        ['python', '-m', 'bci.saver', 'save',
         '-d', _DB_URL, topic, parser_result_json_path],
        stdout=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    assert stdout == b''
    assert stderr is None
