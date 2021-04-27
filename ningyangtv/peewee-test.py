from peewee import *
import json
import os


mysql_db = MySQLDatabase('poemkg', host='localhost', port=3306, user='poem-kg', password='poem-kg')

file = 'poem-dynasty-2.json'
results = open(file, 'r', encoding='utf8')


class PoemKgBase(Model):
    class Meta:
        database = mysql_db


class Poem(PoemKgBase):
    origin = CharField(max_length=20)
    origin_id = IntegerField(null=False, default=-1)
    url = CharField(max_length=200)
    title = CharField(max_length=200)
    content = TextField()
    pingyin = TextField()
    author_id = IntegerField(null=False, default=-1)
    author = CharField(max_length=20)
    author_url = CharField(max_length=200)
    dynasty = CharField(max_length=10)
    translate = TextField()
    shangxi = TextField()


def _save_poems_from_json():
    results = open('poem-dynasty-2.json', 'r', encoding='utf8')
    results.close()
    poems = results.readlines()
    results = open('poem-dynasty-1.json', 'r', encoding='utf8')
    results.close()
    poems.extend(results)

    for poem in poems:
        p = json.loads(poem)
        if '貔貅' in p['content']:
            continue
        p = Poem(
            origin='ningyangtv',
            origin_id=p['id'],
            url=p['url'],
            title=p['title'],
            content=p['content'],
            pingyin=p['pingyin'],
            author_id=p['author_id'],
            author=p['author'],
            author_url=p['author_url'],
            dynasty=p['dynasty'],
            translate=p['translate'],
            shangxi=p['shangxi'],
        )
        try:
            p.save()
        except Exception as ex:
            print(ex)
            print(p)


class Author(PoemKgBase):
    origin = CharField(max_length=20)
    origin_id = IntegerField(null=False, default=-1)
    url = CharField(max_length=200)
    name = CharField(max_length=200)
    dynasty = CharField(max_length=10)
    detail = TextField()


def _save_author_from_file():
    files = ['author-2021-04-22-12_50_23.txt', 'author-2021-04-22-12_57_23.txt', 'author-2021-04-22-13_00_59.txt']
    authors = []
    for file in files:
        f = open(os.path.join(os.pardir, 'results', file), 'r', encoding='utf8')
        authors.extend(f.readlines())
        f.close()
    for author in authors:
        a = json.loads(author)
        a = Author(
            origin='ningyangtv',
            origin_id=a['author_id'],
            url=a['url'],
            dynasty=a['dynasty'],
            name=a['name'],
            detail=a['detail']
        )
        try:
            a.save()
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    # _save_poems_from_json()
    _save_author_from_file()
