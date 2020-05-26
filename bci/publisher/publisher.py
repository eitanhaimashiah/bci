from ..defaults import DEFAULT_URL
from .drivers import find_driver


class Publisher:
    """Represents a message queue publisher.

    Attributes:
        url (str): URL of the message queue's server.
        is_subscriber (bool): If true, this publisher is also a subscriber.

    Args:
        url (:obj:`str`, optional): URL of the message queue's server.
            Default to `DEFAULT_URL`.
        is_subscriber (:obj:`bool`, optional): If true, this publisher
            is also a subscriber. Default to `DEFAULT_IS_SUBSCRIBER`.

    """
    def __init__(self, url=None, is_subscriber=None):
        driver_cls = find_driver(url or DEFAULT_URL)
        self._driver = driver_cls(url, is_subscriber)

    def publish(self, message, exchange, routing_key):
        self._driver.publish(message, exchange, routing_key)

    def subscribe(self, exchange, routing_key, queue, callback):
        self._driver.subscribe(exchange, routing_key, queue, callback)
