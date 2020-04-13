from PIL import Image
from .context import Context
from ..protocol.sample_pb2 import Snapshot


def parse_color_image(context, snapshot):
    """Collects the color image of what the user was seeing at a
    given timestamp from `snapshot`, and publishes the result to a
    dedicated topic.

    Args:
        context (Context): Context in the application.
        snapshot (Snapshot): Snapshot uploaded to the server.

    """
    # TODO Check this function again
    path = context.path(f'color_image.jpg')
    size = snapshot.color_image.width, snapshot.color_image.height
    image = Image.frombytes('RGB', size, snapshot.color_image.data)
    image.save(path)


parse_color_image.field = 'color_image'
