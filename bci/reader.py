import struct
from PIL import Image
from datetime import datetime
from .snapshot import Snapshot


class Reader:
    def __init__(self, path):
        self.path = path
        self._read_user_info()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._read_snapshot()
        except Exception:
            self.fd.close()
            raise StopIteration

    def _read_user_info(self):
        self.fd = open(self.path, 'rb')
        self.user_id = struct.unpack('<Q', self.fd.read(8))[0]
        username_size = struct.unpack('<I', self.fd.read(4))[0]
        self.username = self.fd.read(username_size).decode()
        self.user_birth_date = datetime.fromtimestamp(
            int(struct.unpack('<I', self.fd.read(4))[0]))
        self.user_gender = self.fd.read(1).decode()

    def _read_snapshot(self):
        timestamp = struct.unpack('<Q', self.fd.read(8))[0]
        timestamp /= 1000  # convert `timestamp` from milliseconds to seconds
        translation = struct.unpack('<3d',
                                    self.fd.read(struct.calcsize('<3d')))
        rotation = struct.unpack('<4d',
                                 self.fd.read(struct.calcsize('<4d')))

        # Read the color image.
        color_image_height, color_image_width = struct.unpack('<II',
                                                              self.fd.read(8))
        data = []
        for pixel in range(color_image_height * color_image_width):
            bgr_pixel = self.fd.read(3)
            b, g, r = bgr_pixel
            rgb_pixel = r, g, b
            data.append(rgb_pixel)
        color_image = Image.new('RGB', (color_image_width, color_image_height))
        color_image.putdata(data)

        # Read the depth image.
        depth_image_height, depth_image_width = struct.unpack('<II',
                                                              self.fd.read(8))
        depth_image_size = depth_image_height * depth_image_width
        depth_image_size_format = f'<{depth_image_size}f'
        data = struct.unpack(depth_image_size_format,
                             self.fd.read(struct.calcsize(
                                 depth_image_size_format)))
        depth_image = Image.new('F', (depth_image_width, depth_image_height))
        depth_image.putdata(data)

        user_feelings = struct.unpack('<4f',
                                      self.fd.read(struct.calcsize('<4f')))

        return Snapshot(timestamp,
                        translation,
                        rotation,
                        color_image,
                        depth_image,
                        user_feelings)

    def user_info(self):
        if self.user_gender == 'o':
            gender = 'other'
        else:
            gender = 'male' if self.user_gender == 'm' else 'female'
        return f'user {self.user_id}: {self.username}, ' \
               f'born {self.user_birth_date:%B %-d, %Y} ({gender})'
