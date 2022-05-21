#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author : Liu Kun
# email  : liukunup@163.com
# date   : 2022-05-20 21:59:59

from typing import Optional

from data_access import LocalDatabaseServer
from utils.kit_env import get_database_conf


class DataSource(LocalDatabaseServer):

    def __init__(self, host=None, port=None, username=None, password=None, database=None):
        conf = get_database_conf()
        super().__init__(conf["HOST"] if host is None else host,
                         conf["PORT"] if port is None or not isinstance(port, int) else port,
                         conf["USERNAME"] if username is None else username,
                         conf["PASSWORD"] if password is None else password,
                         conf["DATABASE"] if database is None else database)

    @classmethod
    def get_usage_count(cls) -> Optional[int]:
        """ 获取数据资源用量 """
        print("获取数据资源用量 方法暂未实现!")
        return None

    @classmethod
    def get_remained_count(cls) -> Optional[int]:
        """ 获取数据资源余量 """
        print("获取数据资源余量 方法暂未实现!")
        return None
