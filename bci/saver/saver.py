import furl

from .drivers import find_driver
from ..defaults import DEFAULT_DB_URL, DEFAULT_SETUP, DEFAULT_STR_DATES


class Saver:
    """Represents a database saver.

    Attributes:
        db_url (str): URL of the running database.

    Args:
        db_url (:obj:`str`, optional): URL of the running database.
            Default to `DEFAULT_DB_URL`.
        setup (bool): If true, setups the running database.
            Default to `DEFAULT_SETUP`.

    """

    def __init__(self, db_url=None, setup=None):
        self.db_url = db_url or DEFAULT_DB_URL
        url = furl.furl(self.db_url)
        driver_cls = find_driver(url.scheme)
        if setup is None:
            setup = DEFAULT_SETUP
        self._driver = driver_cls(self.db_url, setup)

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

    def get(self, endpoint, str_dates=None, **kwargs):
        """Gets the rows corresponding to the specified API endpoint
        from the database.

        Args:
            endpoint (str): API endpoint.
            str_dates (bool): If true, converts the dates in the result
                to `str`, according to the appropriate format.
                Default to `DEFAULT_STR_DATES`.
            kwargs (dict): `enpoint`'s arguments

        Returns:
            dict: A dictionary representation of the required rows.

        Raises:
            ValueError: If `endpoint` is unknown.

        """
        if str_dates is None:
            str_dates = DEFAULT_STR_DATES
        return self._driver.get(endpoint, str_dates=str_dates, **kwargs)

    def close(self):
        self._driver.close()
