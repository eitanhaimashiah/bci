import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('agg')


class DepthImageParser:

    field = 'depth_image'

    def parse(self, context, snapshot):
        path = context.path(f'depth_image.jpg')
        size = snapshot.depth_image.height, snapshot.depth_image.width
        plt.imshow(np.reshape(snapshot.depth_image.data, size), cmap='nipy_spectral')
        plt.colorbar()
        # plt.axis('off')
        plt.savefig(path)
        plt.close()
