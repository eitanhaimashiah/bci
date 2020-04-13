class Saver:
    """Encapsulates a database saver.

    Args:
        database_url (str): URL of the running database.

    Attributes:
        database_url (str): URL of the running database.

    """

    def __init__(self, database_url):
        self.database_url = database_url

    def save(self, topic, data):
        """Saves `data` under `topic` in the database.

        Args:
            topic (str): Parser name.
            data (bytes): Raw data, as consumed from the message queue

        """
        # TODO Complete this function
        pass
