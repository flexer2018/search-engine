DROP TABLE domains;
CREATE TABLE domains (id INTEGER PRIMARY KEY AUTOINCREMENT, domain TEXT, last_crawled TEXT);
DROP TABLE pages;
CREATE TABLE pages (id INTEGER PRIMARY KEY AUTOINCREMENT, domain_id INTEGER, url TEXT, path TEXT, content TEXT, last_crawled TEXT);