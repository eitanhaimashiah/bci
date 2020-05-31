import furl

from .drivers import find_driver
from ..defaults import DEFAULT_DB_URL


class Saver:
    """Represents a database saver.

    Attributes:
        db_url (str): URL of the running database.

    Args:
        db_url (:obj:`str`, optional): URL of the running database.
            Default to `DEFAULT_DB_URL`.

    """

    def __init__(self, db_url=None):
        self.db_url = db_url or DEFAULT_DB_URL
        url = furl.furl(self.db_url)
        driver_cls = find_driver(url.scheme)
        self._driver = driver_cls(self.db_url)

    def save(self, topic, data):
        """Saves `data` under `topic` in the database.

        Args:
            topic (str): Topic name.
            data (str): JSON-formatted raw data, as consumed from
            the message queue. The data contains the result received
            from the `topic` parser as well as the corresponding
            snapshot and user information.

        """
        self._driver.save(topic, data)
