#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 2017/9/5
# __author__: caoge
import pymysql

class MysqlConn():
    def __init__(self, host, port, user, password, db, charset="utf8mb4", ):
        config = {
                'host': host,
                'port': port,
                'user': user,
                'password': password,
                'db': db,
                'charset': charset,
                'cursorclass': pymysql.cursors.DictCursor,
        }
        print(config)
        self._conn = pymysql.connect(**config)

    def select(self, sql):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(sql)
                req = cursor.fetchall()
            self._conn.commit()
        finally:
            self._conn.close()
        return req

if __name__ == '__main__':
    mysqld = MysqlConn('127.0.0.1', 3306, 'root', '123456', 'gaga_dota2')
    req = mysqld.select('select count(*) from logic_currentplayers')
    print(req)