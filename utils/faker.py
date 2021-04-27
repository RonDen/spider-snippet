from fake_useragent import UserAgent
import ast
import requests
from requests.models import Response


class Faker:
    def __init__(self, level=0):
        """
        Faker class to fool the server
        :param level: int, which fake level you want to use, default 0, the lowest, do not fake
        0: do not fake
        1: use fake-user-agent to get random headers
        2: use fake-user-agent + proxy-pool, make sure you have started the proxy-pool server
        """
        self.ua = UserAgent()
        self.proxy_api_url = "http://127.0.0.1:5010/get/"
        self.level = level

    def get_headers(self):
        headers = {
            "UserAgent": self.ua.random
        }
        return headers

    def get_proxy(self):
        content = requests.get(self.proxy_api_url).content
        return ast.literal_eval(content.decode('utf8'))

    def faked_get(self, url: str) -> Response:
        if self.level == 0:
            return requests.get(url)
        elif self.level == 1:
            return requests.get(url, headers=self.get_headers())
        else:
            proxy = self.get_proxy()
            return requests.get(url, headers=self.get_headers(), proxies=proxy)
