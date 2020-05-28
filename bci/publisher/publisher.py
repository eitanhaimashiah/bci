import furl

from .drivers import find_driver
from ..defaults import DEFAULT_MQ_URL, DEFAULT_IS_SUBSCRIBER


class Publisher:
    """Represents a message queue publisher.

    Attributes:
        mq_url (str): URL of the message queue's server.
        is_subscriber (bool): If true, this publisher is also a subscriber.

    Args:
        mq_url (:obj:`str`, optional): URL of the message queue's server.
            Default to `DEFAULT_MQ_URL`.
        is_subscriber (:obj:`bool`, optional): If true, this publisher
            is also a subscriber. Default to `DEFAULT_IS_SUBSCRIBER`.

    Raises:
        ValueError: If an invalid URL was provided.

    """
    def __init__(self, mq_url=None, is_subscriber=None):
        self.mq_url = mq_url or DEFAULT_MQ_URL
        self.is_subscriber = is_subscriber or DEFAULT_IS_SUBSCRIBER
        url = furl.furl(self.mq_url)
        driver_cls = find_driver(url.scheme)
        self._driver = driver_cls(url.host, url.port, is_subscriber)

    def publish(self, message, exchange, routing_key):
        """Publishes `message` to the queues on the exchange, while
        routing it by the routing key.

        Args:
            message (str): JSON-formatted message to be published.
            exchange (str): The name of the exchange to publish to.
            routing_key (str): The routing key to bind on.

        """
        self._driver.publish(message, exchange, routing_key)

    def subscribe(self, exchange, routing_key, queue, callback):
        """Subscribes `queue` to `exchange` on `routing_key`, and
        starts the created channel to consume messages.

        Args:
            exchange (str): The name of the exchange to subscribe to.
            routing_key (str): The routing key to bind on.
            queue (str): The queue to consume from.
            callback (callable): The function to call when consuming
                with the following signature:
                callback(channel, method, properties, body)

        """
        self._driver.subscribe(exchange, routing_key, queue, callback)
