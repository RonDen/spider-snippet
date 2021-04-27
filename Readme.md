# My Spider Snippet
我的爬虫片段，记录了编写爬虫时常用到了一些小工具，并对其进行了简单的封装。包括伪造请求头（ 基于 [fake-useragent](https://pypi.org/project/fake-useragent/) ），IP代理池（基于 [proxy-pool](https://github.com/jhao104/proxy_pool) ），正则表达式等小工具，并配被简单的案例提供学习。





## 简单好用的Faker类

```python
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
```

## 爬取案例

- 爬取csdn博客文章：[csdn_spider](./csdn_spider)
- 爬取古诗词信息：[ningyangtv](./ningyangtv)
- 测试selenium工具：[selenium-test](./selenium-test)
- 测试MongoDB Python连接：[mongo-server](./mongo-server)

## 实现细节

对网页的抓取基本使用了requests和bs4两个库来实现，简单明了。
之后采用了Scrapy进行了重构，基于Scrapy的代码见这个[仓库](https://github.com/RonDen/PoemKGSpider/) 。




