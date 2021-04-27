from scrapy import Selector
from bs4 import BeautifulSoup
from bs4.element import Tag

import math
import time
import json
from datetime import datetime
from utils.faker import Faker
from utils.rehelper import reg_int


faker = Faker(level=1)


class Config:
    def __init__(self):
        self.ROOT_URL = 'http://www.ningyangtv.cn'
        self.GUSHI = '/gushi/'
        self.RESULT_FILE = 'poem-dynasty-{}.json'.format(datetime.now().strftime(fmt="%Y%m%D-%H%M"))
        self.FAIL_LIST  = 'fail_list-{}.txt'.format(datetime.now().strftime(fmt="%Y%m%D-%H%M"))
        self.disallow_words = set()
        self.disallow_words.add('貔貅')
        self.log_file = None
        self.failed = None

    def get_page_num(self):
        html_text = faker.faked_get(self.ROOT_URL + self.GUSHI)
        soup = BeautifulSoup(html_text, "html.parser")

        selector = Selector(text=html_text)
        # '共26096首诗词'
        poem_num_str = selector.xpath('/html/body/div[2]/div[1]/div[5]/span/text()').get()

        page_size = 11
        poem_num = reg_int(poem_num_str)
        # poem_num = 26096
        page_num = math.ceil(poem_num / page_size)
        return page_num

    def get_logger(self):
        self.log_file = open(self.RESULT_FILE, 'w', encoding='utf8')
        self.failed = open(self.FAIL_LIST, 'w', encoding='utf8')
        return self.log_file, self.failed

    def log_poem(self, poem: dict):
        self.log_file.write(json.dumps(poem))


cfg = Config()

base_url = 'http://www.ningyangtv.cn/gushi/0/0/0/0/0/{}/'


def _trim_html(tag):
    clist = tag.find_all('span') + tag.find_all('p')
    return '|'.join([c.text.strip() for c in clist]) if clist else tag.text.strip()


# 获取翻译或者赏析的信息
def _get_detail(tag):
    hasa = tag.find('a')
    if hasa:
        url = cfg.ROOT_URL + hasa['href']
        html_doc = faker.faked_get(url)
        soup = BeautifulSoup(html_doc, 'html.parser')
        article = soup.find('dd')
        res = []
        for c in article:
            if c.find('blockquote') == 0:
                continue
            elif isinstance(c, Tag):
                res.append(c.text.strip())
        return '\n'.join(res[1:])
    else:
        return ""


def parser_one_poem(poem_id: int):
    """
    parser one poem page
    :param poem_id: int
    :return:
    """
    url = cfg.ROOT_URL + '/shi/{}.html'.format(poem_id)
    try:
        html_doc = faker.faked_get(url)
        soup = BeautifulSoup(html_doc, 'html.parser')
        article = soup.find('div', attrs={'class': 'article'})
        dds = article.find_all('dd')
        title = article.find('h2').text
        ems = article.find_all('em')
        author_tag = ems[0]
        dynasty_tag = ems[1].find('a')
        content_tag = dds[0]
        pingyin_tag = dds[1]
        translate_tag = dds[2]
        shangxi_tag = dds[3]
        translate = _get_detail(translate_tag)
        shangxi = _get_detail(shangxi_tag)
        content = _trim_html(content_tag)
        pingyin = _trim_html(pingyin_tag)
        poem = {
            'id': poem_id,
            'url': url,
            'title': title,
            'content': content,
            'pingyin': pingyin,
            'author_id': -1,  # -1 means no detail infomation
            'author': author_tag.text[3:],
            'author_url': cfg.ROOT_URL,
            'dynasty': dynasty_tag.text,
            'translate': translate,
            'shangxi': shangxi
        }
        if not author_tag.find('a'):
            poem['author_id'] = -1
            poem['author'] = author_tag.text[3:]
            poem['author_url'] = cfg.ROOT_URL
        else:
            author_href = author_tag.find('a')['href']
            author_id = reg_int(author_href)
            poem['author_id'] = author_id
            poem['author'] = author_tag.text[3:]
            poem['author_url'] = cfg.ROOT_URL + author_href
        cfg.log_file.write(json.dumps(poem))
        cfg.log_file.write('\n')
    except:
        print("Failed in url ", url)
        cfg.failed.write(url)
        cfg.failed.write('\n')


def parser_one_page(url: str):
    """
    Parser one poem list page
    :param url:
    :return:
    """
    html_doc = faker.faked_get(url)
    soup = BeautifulSoup(html_doc, "html.parser")
    poem_list = soup.find_all('strong')
    for li in poem_list:
        href = li.find('a')['href']
        poem_id = reg_int(href)
        parser_one_poem(poem_id)
        time.sleep(0.2)


def start():
    log_filer, failed = cfg.get_logger()
    last_failed_page = 1520
    for i in range(last_failed_page, cfg.get_page_num() + 1):
        url = base_url.format(i)
        parser_one_page(url)
    log_filer.close(), failed.close()


def debug():
    parser_one_poem(62475)


def handle_failure(url:str):
    html_doc = faker.faked_get(url)
    pass


if __name__ == '__main__':
    st = time.time()
    # debug()
    start()
    du = time.time() - st
    print("spend {}h {}m {}s".format(du/3600, du/60, du))


