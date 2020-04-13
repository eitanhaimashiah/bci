import struct
from ....protocol.sample_pb2 import User, Snapshot, \
    Pose, ColorImage, DepthImage, Feelings


class BinaryDriver:
    def __init__(self, path):
        self.file = open(path, 'rb')

    def close_file(self):
        self.file.close()

    def read_user(self):
        user_id, = self._read_field('<Q')
        username_size, = self._read_field('<I')
        username = self.file.read(username_size).decode()
        birthday, = self._read_field('<I')
        genders = {'m': User.MALE, 'f': User.FEMALE, 'o': User.OTHER}
        gender = genders[self.file.read(1).decode()]
        return User(user_id=user_id,
                    username=username,
                    birthday=birthday,
                    gender=gender)

    def read_snapshot(self):
        datetime, = self._read_field('<Q')
        tx, ty, tz = self._read_field('<3d')
        translation = Pose.Translation(x=tx, y=ty, z=tz)
        rx, ry, rz, rw = self._read_field('<4d')
        rotation = Pose.Rotation(x=rx, y=ry, z=rz, w=rw)
        pose = Pose(translation=translation,
                    rotation=rotation)

        # Read the color image.
        color_image_height, color_image_width = self._read_field('<II')
        color_image_data = []
        for pixel in range(color_image_height * color_image_width):
            bgr_pixel = self.file.read(3)
            b, g, r = bgr_pixel
            rgb_pixel = r, g, b
            color_image_data.extend(rgb_pixel)
        color_image = ColorImage(width=color_image_width,
                                 height=color_image_height,
                                 data=bytes(color_image_data))

        # Read the depth image.
        depth_image_height, depth_image_width = self._read_field('<II')
        depth_image_size = depth_image_height * depth_image_width
        depth_image_data = self._read_field(f'<{depth_image_size}f')
        depth_image = DepthImage(width=depth_image_width,
                                 height=depth_image_height,
                                 data=depth_image_data)

        # Read the feelings.
        hunger, thirst, exhaustion, happiness = self._read_field('<4f')
        feelings = Feelings(hunger=hunger,
                            thirst=thirst,
                            exhaustion=exhaustion,
                            happiness=happiness)

        return Snapshot(datetime=datetime,
                        pose=pose,
                        color_image=color_image,
                        depth_image=depth_image,
                        feelings=feelings)

    def _read_field(self, fmt):
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self.file.read(size))
