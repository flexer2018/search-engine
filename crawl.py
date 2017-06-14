import os, sqlite3, subprocess

con = sqlite3.connect('searchengine.db')
cur = con.cursor()
cur.execute('SELECT domain from domains WHERE last_crawled IS NULL')
domains = cur.fetchall()
for domain in domains:
    print("scrapy crawl mainspider -a domain=%s" % domain[0])
    subprocess.call("scrapy crawl mainspider -a domain=%s" % domain[0], shell=True)
