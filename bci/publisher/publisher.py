import pathlib

from .drivers import find_driver
from ..protocol.utils.context import Context
from ..protocol.utils.json_format import json_user, json_snapshot


class Publisher:
    """Represents a message queue handler.

    Attributes:
        url (str): URL of the message queue's server.
        root (str): Root directory of the filesystem shared among all
            containers.

    Args:
        url (str): URL of the message queue's server.
        root (str): Root directory of the filesystem shared among all
            containers.

    """

    def __init__(self, url, root):
        self.url = url
        self.root = pathlib.Path(root)
        self.driver = find_driver(self.url)
        self.context = Context(self.root)

    def __repr__(self):
        return f'{self.__class__.__name__}(' \
               f'url={self.url!r}, ' \
               f'root={self.root!r})'

    def publish(self, message):
        """Publishes `message` to the message queue.

        Args:
            message: Message to be published.

        Raises:
            TODO Complete

        """
        user, snapshot = message

        # TODO Continue from here
        self.driver.share_publish(json_user(user),
                                  routing_key='user',
                                  exchange='results')
        self.context.save_blobs(user, snapshot)
        self.driver.task_publish(json_snapshot(snapshot, user.user_id, self.root),
                                 segment='raw_data')



