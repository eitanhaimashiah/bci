import pytest
import pathlib
import json
import os
import sys
import datetime as dt
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bci.protocol.sample_pb2 as sample
from bci.protocol.utils.to_dict import user_to_dict, snapshot_to_dict
from bci.protocol.utils.parse_serialize import serialize_to_binary_seq
from bci.protocol.utils.display import get_datetime_str
from bci.defaults import FS_ROOT


@pytest.fixture
def root_dir():
    d = FS_ROOT  # TODO If I can modify `bci.defaults.FS_ROOT` to `tmp_path`, it's better
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture
def blobs_dir(root_dir):
    d = root_dir / 'blobs'
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture
def user_snapshot_dirs(user, snapshot):
    return pathlib.Path(str(user.user_id),
                        get_datetime_str(snapshot.datetime, purpose='save'))


@pytest.fixture
def blobs_snapshot_dir(blobs_dir, user_snapshot_dirs):
    d = blobs_dir / user_snapshot_dirs
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture
def raw_data_dir(blobs_snapshot_dir):
    d = blobs_snapshot_dir / 'raw_data'
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture
def results_dir(blobs_snapshot_dir):
    d = blobs_snapshot_dir / 'results'
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture
def snapshots_dir(root_dir):
    d = root_dir / 'snapshots'
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture
def parser_results_dir(root_dir):
    d = root_dir / 'parser_results'
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture
def user():
    birthday = int(dt.datetime(1994, 10, 4).timestamp())
    return sample.User(user_id=10,
                       username='Eitan-Hai Mashiah',
                       birthday=birthday,
                       gender=sample.User.MALE)


@pytest.fixture
def snapshot():
    datetime = int(dt.datetime(2020, 4, 1, 11, 12, 13).timestamp() * 1000)
    translation = sample.Pose.Translation(x=1, y=2, z=3)
    rotation = sample.Pose.Rotation(x=4, y=5, z=6, w=7)
    pose = sample.Pose(translation=translation,
                       rotation=rotation)
    color_image = sample.ColorImage(width=1,
                                    height=2,
                                    data=bytes([1, 2, 3, 4, 5, 6]))
    depth_image = sample.DepthImage(width=1,
                                    height=2,
                                    data=[1, 2])
    feelings = sample.Feelings(hunger=1,
                               thirst=2,
                               exhaustion=3,
                               happiness=4)
    return sample.Snapshot(datetime=datetime,
                           pose=pose,
                           color_image=color_image,
                           depth_image=depth_image,
                           feelings=feelings)


@pytest.fixture
def raw_data(user, snapshot):
    return serialize_to_binary_seq(user, snapshot)


@pytest.fixture
def raw_data_and_path(raw_data, root_dir):
    path = root_dir / 'sample.mind'
    path.write_bytes(raw_data)
    return raw_data, str(path)


@pytest.fixture
def raw_data_dict(user, snapshot, raw_data_dir):
    color_image_path = raw_data_dir / 'color_image'
    color_image_path.write_bytes(snapshot.color_image.data)
    depth_image_path = raw_data_dir / 'depth_image.npy'
    np.save(depth_image_path, snapshot.depth_image.data)
    return {
       'user': user_to_dict(user),
       'snapshot': snapshot_to_dict(snapshot,
                                    color_image_path=str(color_image_path),
                                    depth_image_path=str(depth_image_path))
    }


@pytest.fixture
def raw_data_json(raw_data_dict):
    return json.dumps(raw_data_dict)


@pytest.fixture
def raw_data_json_path(raw_data_json, snapshots_dir):
    path = snapshots_dir / 'snapshot.raw'
    path.write_text(raw_data_json, encoding='utf8')
    return str(path)


@pytest.fixture
def parser_result(topic, raw_data_dict, results_dir):
    user, snapshot = raw_data_dict['user'], raw_data_dict['snapshot']
    if topic == 'pose':
        expected_result = snapshot['pose']
    elif topic == 'color_image' or topic == 'depth_image':
        expected_result = {
            'path': str(results_dir / f'{topic}.jpg')
        }
    elif topic == 'feelings':
        expected_result = snapshot['feelings']
    else:
        expected_result = None
    return {
        'user': user,
        'snapshot': {
            'datetime': snapshot['datetime']
        },
        'result': expected_result
    }


@pytest.fixture
def parser_result_json(topic, parser_result):
    return json.dumps(parser_result)


@pytest.fixture
def parser_result_json_path(topic, parser_result_json, parser_results_dir):
    path = parser_results_dir / f'{topic}.result'
    path.write_text(parser_result_json, encoding='utf8')
    return str(path)
