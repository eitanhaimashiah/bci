import pathlib
from PIL import Image


def parse_color_image(context, snapshot):
    """Collects the color image of what the user was seeing at a given
    timestamp from `snapshot`. The image itself is stored to disk.

    Args:
        context (bci.protocol.utils.Context): Context in the application.
        snapshot (dict): Snapshot as consumed from the message queue
            and converted to dictionary representation.

    Returns:
        dict: A dictionary containing `snapshot`'s color image metadata.

    """
    color_image = snapshot['color_image']
    size = color_image['width'], color_image['height']
    data = pathlib.Path(color_image['data']).read_bytes()
    result_path = context.path('color_image.jpg', is_raw=False)
    image = Image.frombytes('RGB', size, data)
    image.save(result_path)
    return {
        'path': str(result_path)
    }


parse_color_image.field = 'color_image'
