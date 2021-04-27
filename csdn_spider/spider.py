import requests

url_list = [
    'http://www.ningyangtv.cn/',
    'https://www.gushiwen.org/',
    'https://www.shicimingju.com/',
    'http://www.zhonghuashici.com/',
    'https://shici.chazidian.com/',
    'https://www.shici.net/',
    'http://www.haoshiwen.org/'
]

response = requests.get(url_list[0])
print(response.text)