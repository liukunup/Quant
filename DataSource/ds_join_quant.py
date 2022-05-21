#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author : Liu Kun
# email  : liukunup@163.com
# date   : 2022-05-20 21:59:59
# source : 聚宽数据
# see https://www.joinquant.com/help/api/help#name:JQData

from typing import Optional

from jqdatasdk import *
from data_source import DataSource
from DataSource.models import Security


class JoinQuant(DataSource):

    def __init__(self, jq_username, jq_password, host=None, port=None, username=None, password=None, database=None):
        super().__init__(host=host, port=port, username=username, password=password, database=database)
        self.username = jq_username
        self.password = jq_password

    def login(self):
        print("-" * 100)
        print(f"即将登陆账号 {self.username} ...")
        auth(self.username, self.password)
        if not is_auth():
            raise EnvironmentError("认证失败")
        print("认证成功.")
        print("-" * 100)
        return True

    def logout(self):
        print("-" * 100)
        print(f"即将退出账号 {self.username} ...")
        logout()
        if not is_auth():
            print("退出成功.")
            print("-" * 100)
            return True
        else:
            print("退出失败!")
            print("-" * 100)
            return False

    @classmethod
    def get_usage_count(cls) -> Optional[int]:
        """ 获取数据资源用量 """
        count = get_query_count()
        return count["total"] - count["spare"] if count else None

    @classmethod
    def get_remained_count(cls) -> Optional[int]:
        """
        查询当日剩余可调用条数
        1、试用账号默认是每日50万条;
        2、正式账号是每日2亿条。
        注意: 数据库里的一行表示一条!!!
        """
        count = get_query_count()
        return count["spare"] if count else None

    def get_security_by_code(self, code):
        """
        获取股票/基金/指数的信息.
        :param code: 证券代码
        :return: 单个标的信息（股票/基金/指数的信息）
        """
        # 尝试从本地数据库服务器读取
        security = super().get_security_by_code(code=code)
        if security:
            # 如果能读取到直接返回即可
            return security
        else:
            # 读取不到时,先验证是否登陆过
            if is_auth():
                # 通过远程接口获取股票/基金/指数的信息
                dat = get_security_info(code)
                if dat:
                    # 远程能读取到,需要缓存到本地数据库服务器
                    obj = Security(code=dat.code, name=dat.name, display_name=dat.display_name,
                                   start_date=dat.start_date, end_date=dat.end_date,
                                   security_type=dat.type, security_parent=dat.parent)
                    super().save(obj)
                    # 返回读取到的单个标的信息
                    return obj
        # 啥都没搞成则返回None
        return None
