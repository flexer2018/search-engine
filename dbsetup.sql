drop table domains;
create table domains (id integer primary key autoincrement, domain text);
drop table links;
create table links (id integer primary key autoincrement, domain_id integer, link text);