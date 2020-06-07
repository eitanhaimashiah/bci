import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('agg')


def parse_depth_image(context, snapshot):
    """Collects the depth image of what the user was seeing at a given
    timestamp from `snapshot`. The image itself is stored to disk.

    Args:
        context (bci.protocol.utils.Context): Context in the application.
        snapshot (dict): Snapshot as consumed from the message queue
            and converted to dictionary representation.

    Returns:
        dict: A dictionary containing `snapshot`'s depth image metadata.

    """
    depth_image = snapshot['depth_image']
    size = depth_image['height'], depth_image['width']
    data = np.load(depth_image['data']).reshape(size)
    result_path = context.path('depth_image.jpg', is_raw=False)
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.savefig(result_path)
    plt.close()
    return {
        'path': str(result_path)
    }


parse_depth_image.field = 'depth_image'
