from ...protocol import sample_pb2 as pb
from ...utils.struct import read_by_format


class BinaryDriver:
    """Represents a driver to read sample files of binary format.

    Attributes:
        stream (IOBase): Stream representing the sample file.

    """

    def __init__(self, stream):
        self.stream = stream

    def read_user(self):
        user_id, = self._read_field('<Q')
        username_size, = self._read_field('<I')
        username = self.stream.read(username_size).decode()
        birthday, = self._read_field('<I')
        genders = {'m': pb.User.MALE, 'f': pb.User.FEMALE, 'o': pb.User.OTHER}
        gender = genders[self.stream.read(1).decode()]
        return pb.User(user_id=user_id,
                       username=username,
                       birthday=birthday,
                       gender=gender)

    def read_snapshot(self):
        datetime, = self._read_field('<Q')
        tx, ty, tz = self._read_field('<3d')
        translation = pb.Pose.Translation(x=tx, y=ty, z=tz)
        rx, ry, rz, rw = self._read_field('<4d')
        rotation = pb.Pose.Rotation(x=rx, y=ry, z=rz, w=rw)
        pose = pb.Pose(translation=translation,
                       rotation=rotation)

        # Read the color image.
        color_image_height, color_image_width = self._read_field('<II')
        color_image_data = []
        for pixel in range(color_image_height * color_image_width):
            bgr_pixel = self.stream.read(3)
            b, g, r = bgr_pixel
            rgb_pixel = r, g, b
            color_image_data.extend(rgb_pixel)
        color_image = pb.ColorImage(width=color_image_width,
                                    height=color_image_height,
                                    data=bytes(color_image_data))

        # Read the depth image.
        depth_image_height, depth_image_width = self._read_field('<II')
        depth_image_size = depth_image_height * depth_image_width
        depth_image_data = self._read_field(f'<{depth_image_size}f')
        depth_image = pb.DepthImage(width=depth_image_width,
                                    height=depth_image_height,
                                    data=depth_image_data)

        # Read the feelings.
        hunger, thirst, exhaustion, happiness = self._read_field('<4f')
        feelings = pb.Feelings(hunger=hunger,
                               thirst=thirst,
                               exhaustion=exhaustion,
                               happiness=happiness)

        return pb.Snapshot(datetime=datetime,
                           pose=pose,
                           color_image=color_image,
                           depth_image=depth_image,
                           feelings=feelings)

    def _read_field(self, format):
        return read_by_format(self.stream, format)
