#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author : Liu Kun
# email  : liukunup@163.com
# date   : 2022-05-20 21:59:59
# source : 聚宽数据
# see https://www.joinquant.com/help/api/help#name:JQData

import pandas as pd

from typing import Optional, Any, List

from jqdatasdk import *
from DataSource.data_source import DataSource
from DataSource.models import Security
from utils.kit_env import get_join_quant_conf


class JoinQuant(DataSource):

    def __init__(self, jq_username=None, jq_password=None,
                 host=None, port=None, username=None, password=None, database=None):
        super().__init__(host=host, port=port, username=username, password=password, database=database)
        # 尝试默认配置
        conf = get_join_quant_conf()
        self.username = conf["USERNAME"] if jq_username is None else jq_username
        self.password = conf["PASSWORD"] if jq_password is None else jq_password

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

    def get_security_info(self, code: Any, date: Any = None) -> Optional[Security]:
        # 尝试从本地数据库服务器读取
        security = super().get_security_info(code=code, date=date)
        if security:
            # 如果能读取到直接返回即可
            return security
        else:
            # 读取不到时,先验证是否登陆过
            if is_auth():
                # 通过远程接口获取股票/基金/指数的信息
                dat = get_security_info(code=code, date=date)
                if dat:
                    # 远程能读取到,需要缓存到本地数据库服务器
                    obj = Security(code=dat.code, name=dat.name, display_name=dat.display_name,
                                   start_date=dat.start_date, end_date=dat.end_date,
                                   security_type=dat.type, security_parent=dat.parent)
                    super().insert_or_update(obj)
                    # 返回读取到的单个标的信息
                    return obj
        # 啥都没搞成则返回None
        return None

    def get_all_securities(self, types: List = None, date: Any = None) -> Optional[pd.DataFrame]:
        # 默认为None时转为空列表
        if types is None: types = list()
        # 尝试从本地数据库服务器读取
        securities = super().get_all_securities(types=types, date=date)
        if not securities.empty:
            # 如果能读取到直接返回即可
            return securities
        else:
            # 读取不到时,先验证是否登陆过
            if is_auth():
                # 通过远程接口获取股票/基金/指数的信息列表
                df = get_all_securities(types=types, date=date)
                if not df.empty:
                    for index, row in df.iterrows():
                        obj = Security(code=index, name=row["name"], display_name=row["display_name"],
                                       start_date=row["start_date"], end_date=row["end_date"],
                                       security_type=row["type"])
                        super().insert_or_update(obj)
                return df
        return None

    def get_price(self, security, start_date=None, end_date=None, count=None, frequency='daily', fields=None,
                  skip_paused=False, fill_paused=True, fq='pre',  panel=True):
        return super().get_price(security=security, start_date=start_date, end_date=end_date, count=count,
                                 frequency=frequency, fields=fields, skip_paused=False, fill_paused=True,
                                 fq='pre', panel=True)
