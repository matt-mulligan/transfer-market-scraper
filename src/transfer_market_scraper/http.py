import time
import random
import requests
from pyapp.conf import settings

from transfer_market_scraper.exceptions import LoginError
from transfer_market_scraper.utils import decode


class BaseHttpSession(object):
    """
    Basic HTTP Session Class object.
    """

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/92.0.4515.107 Safari/537.36"
        }

    def get(self, url: str, headers: dict = None, delay_min: int = 10, delay_max: int = 45) -> requests.Response:
        """
        generic get method that uses the classes request.Session object and allows for random delay intervals to be
        used.

        :param url: URL to post to
        :param headers: Header dictionary to use in the request. uses default class headers if not given.
        :param delay_min: minimum amount of time to wait, in seconds, before sending this request
        :param delay_max: maximum amount of time to wait, in seconds before sending this request
        :return: the requests.Response object from the submitted request
        """

        if headers is None:
            headers = self.headers

        self._delay_response(delay_min, delay_max)
        return self.session.get(url, headers=headers)

    def post(
            self, url: str, headers: dict = None, payload: dict = None, delay_min: int = 10, delay_max: int = 45
    ) -> requests.Response:
        """
        generic post method that uses the classes request.Session object and allows for random delay intervals to be
        used.

        :param url: URL to post to
        :param headers: Header dictionary to use in the request. uses default headers if not given.
        :param payload: Payload to post to the url.
        :param delay_min: minimum amount of time to wait, in seconds, before sending this request
        :param delay_max: maximum amount of time to wait, in seconds before sending this request
        :return: the requests.Response object from the submitted request
        """

        if headers is None:
            headers = self.headers

        self._delay_response(delay_min, delay_max)
        return self.session.post(url, headers=headers, data=payload)

    @staticmethod
    def _delay_response(delay_min: int, delay_max: int) -> None:
        """
        method to implement a random sleep interval before sending a request.
        Sets a random int between delay min and delay max, then adds random millisecond values to sleep.

        :param delay_min: integer describing the minimum seconds the sleep could be
        :param delay_max: integer describing the maximum seconds the sleep could be.
        :return: None
        """

        if not delay_min and not delay_max:
            value = 0
        else:
            value = random.randint(delay_min, delay_max) + random.random()

        time.sleep(value)


class GameHttpSession(BaseHttpSession):
    """
    Http Session Class specific to the game, implementing the base Http Class.
    Should always interact via the base classes get/post methods
    """

    def __init__(self):
        super().__init__()
        self.headers_login = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "max-age=0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.url_base = decode(settings.URL_BASE)

    def login(self, user: str, pw: str) -> requests.Response:
        """
        Logs the session object into the website.

        :param user: the username to login as
        :param pw: the password to login for that user. Not sure of a more secure way to do this
        :return: returns the response object from requests.session object.
        """

        url = f"{self.url_base}/nl/login.asp"
        headers = {**self.headers, **self.headers_login}
        payload = {'username': user, 'password': pw}

        response = self.post(url, headers=headers, payload=payload)

        if response.url == f"{self.url_base}/nl/login.asp":
            raise LoginError("Login has failed for the game website")

        return response
