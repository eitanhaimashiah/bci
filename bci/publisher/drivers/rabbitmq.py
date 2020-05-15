import pika
import furl

from defaults import DEFAULT_RABBITMQ_SERVER_HOST, DEFAULT_RABBITMQ_SERVER_PORT

# TODO Replace the following code
def _setup(host, port):
    return None, None


def _exchange_declare(channel, exchange, exchange_type):
    pass


class RabbitmqPublisher:
    """Represents a driver to handle a message queue of RabbitMQ scheme.

    Attributes:
        url (str): URL of the message queue's server.

    Args:
        url (str): URL of the message queue's server.

    Raises:
        TODO Complete.

    """

    scheme = 'rabbitmq'

    def __init__(self, url):
        url = furl.furl(url)
        self.host = url.host or DEFAULT_RABBITMQ_SERVER_HOST
        self.port = url.port or DEFAULT_RABBITMQ_SERVER_PORT

    def share_publish(self, message, exchange, routing_key):
        """Shares `message` to the queue on `exchange`, while routing
        it by `routing_key`.

        The message will be distributed to any active consumers (those
        subscribed to `routing_key`) when the transaction, if any,
        is committed.

        Args:
            message (str): JSON-formatted message to be published.
            exchange (str): The name of the exchange to publish to.
            routing_key (str): Routing key for the message.

        Returns:
            TODO Continue from here

        Raises:
            TODO Complete

        """
        connection, channel = _setup(self.host, self.port)
        # Message is published to all queues binded to exchange
        _exchange_declare(channel, exchange=exchange,
                          exchange_type='direct')

        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=message)
        connection.close()


