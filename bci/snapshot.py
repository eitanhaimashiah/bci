from datetime import datetime


class Snapshot:
    def __init__(self,
                 timestamp,
                 translation,
                 rotation,
                 color_image,
                 depth_image,
                 user_feelings):

        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.user_feelings = user_feelings

    def __str__(self):
        dtime = datetime.fromtimestamp(self.timestamp)
        color_image_width, color_image_height = self.color_image.size
        depth_image_width, depth_image_height = self.depth_image.size
        return f'Snapshot from {dtime:%B %-d, %Y at %H:%M:%S.%f} ' \
               f'on {self.translation} / {self.rotation} ' \
               f'with a ' \
               f'{color_image_width}x{color_image_height} color image ' \
               f'and a ' \
               f'{depth_image_width}x{depth_image_height} depth image.'
