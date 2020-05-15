import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('agg')


def parse_depth_image(context, snapshot):
    """Collects the depth image of what the user was seeing at a
    given timestamp from `snapshot`, and publishes the result to a
    dedicated topic.

    Args:
        context (Context): Context in the application.
        snapshot (Snapshot): Snapshot uploaded to the server.

    """
    # TODO Check this function again
    path = context.path(f'depth_image.jpg')
    size = snapshot.depth_image.height, snapshot.depth_image.width
    plt.imshow(np.reshape(snapshot.depth_image.data, size), cmap='nipy_spectral')
    plt.colorbar()
    # plt.axis('off')
    plt.savefig(path)
    plt.close()


parse_depth_image.field = 'depth_image'
