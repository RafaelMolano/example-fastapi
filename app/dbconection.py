import MySQLdb
import MySQLdb.cursors

class DBHelper:

    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = "root"
        self.db = "pythonapi"
        self.port = 3307

    def __connect__(self):
        self.con = MySQLdb.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port, cursorclass=MySQLdb.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql, params):
        self.__connect__()
        self.cur.execute(sql, params)
        self.con.commit()
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def fetchone(self, sql, params):
        self.__connect__()
        try:
            self.cur.execute(sql, params)
            self.con.commit()
            result = self.cur.fetchone()
            self.__disconnect__()
        except BaseException:
            if self.cur is not None:
                self.cur.rollback()
        return result

    def cursor(self):
        try:
            return self.conn.cursor()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            return self.conn.cursor()

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()

    def hola(self, sql):
        print(sql)    