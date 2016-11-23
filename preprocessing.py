# -*- coding: utf-8 -*-
import pymysql
import os
import sys


class Processing:
    def __init__(self, name, password, db, host):
        """
        Connect to mysql
        """
        self.db = pymysql.connect(
            user=os.getenv('MYSQL_USERNAME', name),
            passwd=os.getenv('MYSQL_PASSWORD', password),
            db=os.getenv('MYSQL_INSTANCE_NAME', db),
            host=os.getenv('MYSQL_PORT_3306_TCP_ADDR', host),
            port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT', '3306')),
            charset='utf8',
            use_unicode=False,
            init_command='SET NAMES UTF8'
        )
        check_connection = self.db.cursor()
        print("connection success!!")
        print(sys.stdin.encoding)
