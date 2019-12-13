import struct
import time
from datetime import datetime


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'{self.__class__.__name__}' \
               f'(user_id={self.user_id}, ' \
               f'timestamp={self.timestamp!r}, ' \
               f'thought={self.thought!r})'

    def __str__(self):
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return f'[{timestamp_str}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        return isinstance(other, Thought) \
               and self.user_id == other.user_id \
               and self.timestamp == other.timestamp \
               and self.thought == other.thought

    def serialize(self):
        timestamp = int(time.mktime(self.timestamp.timetuple()))
        thought_size = len(self.thought)
        thought_utf = self.thought.encode()
        return struct.pack('LLI',
                           self.user_id,
                           timestamp,
                           thought_size) + thought_utf

    @classmethod
    def deserialize(cls, data):
        header_size = struct.calcsize('LLI')
        header, thought_utf = data[:header_size], data[header_size:]
        user_id, timestamp, thought_size = struct.unpack('LLI', header)
        timestamp = datetime.fromtimestamp(timestamp)
        thought = thought_utf.decode()
        return Thought(user_id, timestamp, thought)
