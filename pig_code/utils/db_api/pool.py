import datetime
import json

import mysql.connector
from mysql.connector import pooling

from ...core import *
from ..functions import Func
from ...core.config import users_schema, shop_schema


class MySQLPool:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if MySQLPool.__instance is None:
            MySQLPool()
        return MySQLPool.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.pools = []
        # if MySQLPool.__instance is not None:
        #     raise Exception("This class is a singleton!")
        # else:
        #     MySQLPool.__instance = self
        #     self.pools.append(pooling.MySQLConnectionPool(
        #         pool_name="mypool",
        #         pool_size=32,
        #         host=config.mysql_info['host'],
        #         port=config.mysql_info['port'],
        #         user=config.mysql_info['user'],
        #         password=config.mysql_info['password'],
        #         database=config.mysql_info['database'],
        #         charset='utf8'
        #     ))

    def create_pool(self):
        MySQLPool.__instance = self
        self.pools.append(pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=32,
            host=config.mysql_info['host'],
            port=config.mysql_info['port'],
            user=config.mysql_info['user'],
            password=config.mysql_info['password'],
            database=config.mysql_info['database'],
            charset='utf8'
        ))

    def get_connection(self):
        # print(self.pools)
        for i in range(len(self.pools)):
            try:
                return self.pools[i].get_connection()
            except:
                continue
        else:
            self.create_pool()
            for i in range(len(self.pools)):
                try:
                    return self.pools[i].get_connection()
                except:
                    continue


pool = MySQLPool()
