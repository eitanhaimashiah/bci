import json
from PIL import Image


def parse_color_image(context, snapshot):
    """Collects the color image of what the user was seeing at a
    given timestamp from `snapshot`, and publishes the result to a
    dedicated topic.

    Args:
        context (Context): Context in the application.
        snapshot (Snapshot): Snapshot uploaded to the server.

    """
    # TODO Check this function again
    # Save metadata
    context.save('color_image.json', json.dumps(dict(
        width=snapshot.color_image.width,
        height=snapshot.color_image.height,
        data_path=''
    )))

    # Save data
    path = context.path('color_image_data.jpg')
    size = snapshot.color_image.width, snapshot.color_image.height
    image = Image.frombytes('RGB', size, snapshot.color_image.data)
    image.save(path)


parse_color_image.field = 'color_image'
