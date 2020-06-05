import pytest
import json
import subprocess

from bci.parsers import parse

_TOPICS = ['pose', 'color_image', 'depth_image', 'feelings']


@pytest.mark.parametrize('topic', _TOPICS)
def test_parse_pose(topic, raw_data_json, parser_result):
    result = parse(topic, raw_data_json)
    assert json.loads(result) == parser_result


@pytest.mark.parametrize('topic', _TOPICS)
def test_cli(topic, raw_data_json_path, parser_result):
    process = subprocess.Popen(
        ['python', '-m', 'bci.parsers', 'parse', topic, raw_data_json_path],
        stdout=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert json.loads(stdout) == parser_result
