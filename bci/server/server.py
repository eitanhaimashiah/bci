from flask import Flask, request
from ..utils.sample.sample_pb2 import AssociatedSnapshot
from ..utils.context import Context
from .. import parsers
from ..parsers import parse_pose, parse_feelings, \
    ColorImageParser, DepthImageParser


def _flatten(l):
    gather = []
    for item in l:
        if isinstance(item, tuple):
            gather.extend(item)
        else:
            gather.append(item)
    return gather


def run_server(host, port):
    """Run the server."""
    app = Flask(__name__)
    context = Context()
    user_snapshot = AssociatedSnapshot()
    color_image_parser = ColorImageParser()
    depth_image_parser = DepthImageParser()
    fields = list(set(_flatten(list(map(lambda x: x.field,
                                        parsers.__all__))))) + ['datetime']

    @app.route('/config', methods=['GET'])
    def get_config():
        print(fields)
        # return jsonify({'fields': fields, 'return_value': 3, 'error': None})
        return {'fields': fields}

    @app.route('/snapshot', methods=['POST'])
    def post_snapshot():
        user_snapshot.ParseFromString(request.data)
        user = user_snapshot.user
        snapshot = user_snapshot.snapshot
        context.set(user.user_id, snapshot.datetime)

        # Apply parsers
        parse_pose(context, snapshot)
        parse_feelings(context, snapshot)
        color_image_parser.parse(context, snapshot)
        depth_image_parser.parse(context, snapshot)

        # return jsonify({'return_value': 3, 'error': None})
        return {}

    app.run(host=host, port=port, debug=True)
