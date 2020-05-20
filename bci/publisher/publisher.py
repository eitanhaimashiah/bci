from ..defaults import DEFAULT_URL
from .drivers import find_driver


class Publisher:
    """Represents a message queue publisher.

    Attributes:
        url (str): URL of the message queue's server.

    Args:
        url (:obj:`str`, optional): URL of the message queue's server.
            Default to `DEFAULT_URL`.

    """

    def __init__(self, url=None):
        self.url = url or DEFAULT_URL
        self._driver = find_driver(self.url)

    def publish(self, message, exchange, routing_key):
        self._driver.publish(message, exchange, routing_key)

    def subscribe(self, exchange, routing_key, queue, callback):
        self._driver.subscribe(exchange, routing_key, queue, callback)
