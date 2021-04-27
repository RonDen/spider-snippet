import requests
from fake_useragent import UserAgent
import random

ua = UserAgent()
url = 'http://www.ningyangtv.cn/shi/5872.html'

headers = {
    "User-Agent": ua.random
}

res = requests.get(url, headers=headers)

