import pika


class RabbitmqDriver:
    """Represents a RabbitMQ message-broker driver.

    Attributes:
        host (str): RabbitMQ server's IP address.
        port (int): RabbitMQ server's port.
        is_subscriber (bool): If true, this publisher is also a subscriber.

    Args:
        host (str): RabbitMQ server's IP address.
        port (int): RabbitMQ server's port.
        is_subscriber (bool): If true, this publisher is also a subscriber.

    Raises:
        ValueError: If an invalid URL was provided.

    """

    scheme = 'rabbitmq'

    def __init__(self, host, port, is_subscriber):
        self.host = host
        self.port = port
        self.is_subscriber = is_subscriber

    def publish(self, message, exchange, routing_key):
        """Publishes `message` to the queues on the exchange, while
        routing it by the routing key.

        Args:
            message (str): JSON-formatted message to be published.
            exchange (str): The name of the exchange to publish to.
            routing_key (str): The routing key to bind on.

        Raises:
            AssertionError: If this driver is not a publisher.
            exceptions.ChannelWrongStateError: If the created channel
                is not in the OPEN state.

        """
        connection, channel = self._create_connection(exchange)
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2)  # make `message` persistent
                              )
        print(f'[x] Sent {message!r}')
        connection.close()

    def subscribe(self, exchange, routing_key, queue, callback):
        """Subscribes `queue` to `exchange` on `routing_key`, and
        starts the created channel to consume messages.

        Args:
            exchange (str): The name of the exchange to subscribe to.
            routing_key (str): The routing key to bind on.
            queue (str): The queue to consume from.
            callback (callable): The function to call when consuming
                with the following signature:
                callback(channel: pika.Channel,
                         method: pika.spec.Basic.Deliver,
                         properties: pika.spec.BasicProperties,
                         body:bytes)

        Raises:
            AssertionError: If this driver is not a subscriber.
            exceptions.ChannelWrongStateError: If the created channel
                is not in the OPEN state.

        """
        assert self.is_subscriber, 'cannot subscribe, this driver is not a subscriber'
        connection, channel = self._create_connection(exchange)
        channel.queue_declare(queue, durable=True)
        channel.queue_bind(exchange=exchange,
                           queue=queue,
                           routing_key=routing_key)
        channel.basic_consume(queue=queue,
                              on_message_callback=RabbitmqDriver._on_message_callback(callback))
        try:
            print('[*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()

    def _create_connection(self, exchange):
        """Creates a new connection with the RabbitMQ server.

        Args:
            exchange (str): The name of the exchange to
                publish/subscribe to.

        Returns:
            tuple: Tuple containing:
                connection (pika.BlockingConnection): Created connection.
                channel (pika.channel.Channel): `connection`’s channel.

        Raises:
            exceptions.ChannelWrongStateError: If the created channel
                is not in the OPEN state.

        """
        params = pika.ConnectionParameters(host=self.host, port=self.port)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange,
                                 exchange_type='topic')
        return connection, channel

    @staticmethod
    def _on_message_callback(callback):
        def wrapper(channel, method, properties, body):
            callback(channel, method, properties, body)
            print(f'[x] Received {body}')
            channel.basic_ack(delivery_tag=method.delivery_tag)
        return wrapper
