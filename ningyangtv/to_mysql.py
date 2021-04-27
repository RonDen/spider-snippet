import pymysql.cursors
import json

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='poem-kg',
                             password='poem-kg',
                             database='poemkg',
                             cursorclass=pymysql.cursors.DictCursor)

results = open('poem-dynasty-1.json', 'r', encoding='utf8')

with connection:
    with connection.cursor() as cursor:
        # Create a new record
        poems = results.readlines()
        for poem in poems:
            p = json.loads(poem)
            if '貔貅' in p['content']:
                continue
            sql = "INSERT INTO `poem` (" \
                  "`from`," \
                  "`from_id`," \
                  "`url`," \
                  "`title`," \
                  "`content`," \
                  "`pingyin`," \
                  "`author_id`," \
                  "`author`," \
                  "`author_url`," \
                  "`dynasty`," \
                  "`translate`," \
                  "`shangxi`" \
                  ") VALUES ('%s', %d, '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s', '%s')" % ('ningyangtv',
                    p['id'],
                    p['url'],
                    p['title'],
                    p['content'],
                    p['pingyin'],
                    p['author_id'],
                    p['author'],
                    p['author_url'],
                    p['dynasty'],
                    p['translate'],
                    p['shangxi'])
            try:
                cursor.execute(sql)
            except Exception as ex:
                print(p)
                print(ex)
                exit()


    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    # with connection.cursor() as cursor:
    #     # Read a single record
    #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
    #     cursor.execute(sql, ('webmaster@python.org',))
    #     result = cursor.fetchone()
    #     print(result)