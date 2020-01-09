import struct
from datetime import datetime


class Hello:
    def __init__(self, user_id, username, birth_date, gender):
        self.user_id = user_id
        self.username = username
        self.birth_date = birth_date
        self.gender = gender

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'(user_id={self.user_id}, ' \
               f'username={self.username!r}, ' \
               f'birth_date={self.birth_date!r}, ' \
               f'gender={self.gender!r})'

    def __str__(self):
        if self.gender == 'o':
            g = 'other'
        else:
            g = 'male' if self.gender == 'm' else 'female'
        return f'user {self.user_id}: {self.username}, ' \
               f'born {self.birth_date:%B %-d, %Y} ({g})'

    def __eq__(self, other):
        return isinstance(other, Hello) \
               and self.user_id == other.user_id \
               and self.username == other.username \
               and self.birth_date == other.birth_date \
               and self.gender == other.gender

    def serialize(self):
        username_size = len(self.username)
        username_utf = self.username.encode()
        birth_date_timestamp = int(self.birth_date.timestamp())
        return struct.pack(f'<QI{username_size}sIc',
                           self.user_id,
                           username_size,
                           username_utf,
                           birth_date_timestamp,
                           self.gender)

    @classmethod
    def deserialize(cls, data):
        header_size = struct.calcsize('QQI')


class Config:
    def __init__(self, fields):
        self.fields = fields


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
