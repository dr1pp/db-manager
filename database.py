import sqlite3

class Database:
    """Class used to handle database information

     - .tables is a list of Table objects for every table in the database

    Does not intrinsically represent a specific database, more a structure to handle mutliple databases and switching between them
    """

    def __init__(self):
        self.file_set = False
        self.tables = None
        self.conn = None
        self.cur = None

    def execute(self, query, parameters=None):
        """"""
        if parameters is None:
            self.cur.execute(query)
        else:
            self.cur.execute(query, parameters)
            self.save()

    def set_file(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()
        self.file_set = True

    def get_table_names(self):
        self.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        names = [name[0] for name in self.cur.fetchall()]
        return names

    def get_tables(self):
        tables = [Table(self, name) for name in self.get_table_names()]
        return tables

    def save(self):
        self.conn.commit()


class Table:
    def __init__(self, db, name):
        self.db = db
        self.name = name

    def get_headers(self):
        self.db.execute(f'PRAGMA table_info({self.name})')
        headers = [info[1] for info in self.db.cur.fetchall()]
        return headers

    def get_contents(self):
        self.db.execute(f"SELECT * FROM {self.name}")
        contents = self.db.cur.fetchall()
        return contents