# Web crawler, indexer and search engine

- Demonstration of webcrawling (using scrapy), index(using sqlite and elasticsearch) with a front end (using flask).

Requirements
-----------------

- Tested with Python 3.5 on Ubuntu
- Requires elasticsearch
- See requirements.txt file for required python packages. To install them run `pip install -r /path/to/requirements.txt`
- Also requires sqlite3 which can't be installed with pip

Usage
-------------

- Elasticsearch must be running for the webcrawling storage and web interface to work

### Database setup

- To setup sqlite database:

```bash
sqlite3 searchengine.db
```

```sql
DROP TABLE domains;
CREATE TABLE domains (id INTEGER PRIMARY KEY AUTOINCREMENT, domain TEXT, last_crawled TEXT);
DROP TABLE pages;
CREATE TABLE pages (id INTEGER PRIMARY KEY AUTOINCREMENT, domain_id INTEGER, url TEXT, path TEXT, content TEXT, last_crawled TEXT);
```

### Crawling

To run the spider for a domain run the following:

```bash
scrapy crawl full_site_spider -a domain=domain.com
```

### Search interface

To run the front end search interface run:
```bash
export FLASK_APP=app.py
flask run
```