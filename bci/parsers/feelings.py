import json
from .context import Context
from ..protocol.sample_pb2 import Snapshot


def parse_feelings(context, snapshot):
    """Collects the feelings the user was experiencing at a given
    timestamp from `snapshot`, and publishes the result to a dedicated
    topic.

    Args:
        context (Context): Context in the application.
        snapshot (Snapshot): Snapshot uploaded to the server.

    """
    # TODO Check this function again
    context.save('feelings.json', json.dumps(dict(
        hunger=snapshot.feelings.hunger,
        thirst=snapshot.feelings.thirst,
        exhaustion=snapshot.feelings.exhaustion,
        happiness=snapshot.feelings.happiness
    )))


parse_feelings.field = 'feelings'
