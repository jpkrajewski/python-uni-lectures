import pymysql
from pymysql.constants import CLIENT

from config import Config


class Database:
    def __init__(self, config_file='config.ini'):
        config = Config(config_file)
        self.host = config.get_param('host')
        self.port = int(config.get_param('port'))
        self.user = config.get_param('user')
        self.password = config.get_param('password')
        self.db = config.get_param('database')

    def conn(self):
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            client_flag=CLIENT.MULTI_STATEMENTS  # allow executing multiple queries
        )

    def exec(self, sql):
        ok = False
        try:
            conn = self.conn()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            ok = True
        except pymysql.connect.Error as error:
            print("ERROR:", error)
        finally:
            if conn.ping():
                cur.close()
                conn.close()

        return ok

    def fetch(self, sql):
        conn = self.conn()
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return res
