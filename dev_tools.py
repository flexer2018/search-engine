import sqlite3

class Db(object):

    def __init__(self):
        self.con = sqlite3.connect('searchengine.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

db = Db()