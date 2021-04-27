from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import Tag
import json
import os
import sys
sys.path.append('../')

from utils.faker import Faker
from utils.logger import log
from utils.my_exceptions import NoDataError, ParseError, NotFindError404


class AuthorSpider:
    def __init__(self):
        self.base_url = 'http://www.ningyangtv.cn/shiren/'
        self.num = 1296

        self.result_file = '../results/author-{}.txt'.format(datetime.now().strftime("%Y-%m-%d-%H_%M_%S"))
        self.fail_file = '../fails/author-fail-{}.txt'.format(datetime.now().strftime("%Y-%m-%d-%H_%M_%S"))
        self.faker = Faker()
        self.result_logger = open(self.result_file, 'w', encoding='utf8')
        self.failed_logger = open(self.fail_file, 'w', encoding='utf8')

    def _parse_author_detail(self, author_detail_tag: Tag) -> (str, str):
        """
        Parse the author detail
        :param author_detail_tag: bs4 tag, may contain <p></p> or <br />, I have replaced <br /> by `|`
        :return: detail_content: str, and img_url: str
        """
        img_url = ''
        if author_detail_tag.find('img'):
            img_url = author_detail_tag.find('img')['src']
        if author_detail_tag.text.find('|'):
            ps = author_detail_tag.text.split('|')
            return '\n'.join([p.strip() for p in ps]), img_url
        else:
            ps = author_detail_tag.find_all('p')
            return '\n'.join([p.text.strip() for p in ps]), img_url

    def _parse_one_author(self, author_id: int):
        url = 'http://www.ningyangtv.cn/shiren/{}.html'.format(author_id)
        # url = 'http://www.ningyangtv.cn/shiren/3000.'
        try:
            response = self.faker.faked_get(url)
            if response.status_code == 404:
                raise NotFindError404(url)
            html_doc = response.text
            if html_doc.find('您指定的数据没有找到！') != -1:
                raise NoDataError(url)
            html_doc = html_doc.replace('<br />', '|')
            soup = BeautifulSoup(html_doc, 'html.parser')
            article = soup.find("div", attrs={'class': 'article'})
            name = article.find('h2').text.split(' ')[0]
            dynasty = article.find('em').find('a').text
            detail, img_url = self._parse_author_detail(article.find('dd'))
            author = {
                'author_id': author_id,
                'url': url,
                'dynasty': dynasty,
                'name': name,
                'detail': detail,
            }
            return author
        except NoDataError:
            raise NoDataError(url)
        except NotFindError404:
            raise NotFindError404(url)
        except Exception:
            raise ParseError(url)

    @log
    def start(self):
        i = 706
        while i < 3000:
            url = 'http://www.ningyangtv.cn/shiren/{}.html'.format(i)
            try:
                author = self._parse_one_author(i)
                self.result_logger.write(json.dumps(author, ensure_ascii=False))
                self.result_logger.write('\n')
            except NoDataError as ne:
                print(ne)
            except NotFindError404 as not_find:
                print(not_find)
                break
            except ParseError as pe:
                self.failed_logger.write(url)
                self.failed_logger.write('\n')
                print(pe)
            i += 1

        self.result_logger.close()
        self.failed_logger.close()

    def debug(self, author_id: int):
        try:
            author = self._parse_one_author(author_id)
            print(author)
        except NoDataError as ne:
            print(ne)
        except ParseError as pe:
            print(pe)
        except NotFindError404 as not_find:
            print(not_find)


if __name__ == '__main__':
    spider = AuthorSpider()
    spider.start()
    # spider.debug(3000)
