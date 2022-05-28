#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author : Liu Kun
# email  : liukunup@163.com
# date   : 2022-05-21 12:00:00
# source : 本地 数据库接入层
# see https://docs.sqlalchemy.org/en/14/index.html#

import pandas as pd

from typing import Optional, Any, List
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from jqdatasdk.utils import *

from DataSource import Base
from DataSource.models import Security, Price


class LocalDatabaseServer:

    def __init__(self, host, port, username, password, database):
        self.engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}", future=True)
        self.session = sessionmaker(bind=self.engine, future=True)

    def create_all(self):
        """ 创建所有表 """
        # 请谨慎使用
        Base.metadata.create_all(bind=self.engine)

    def destroy_all(self):
        """ 销毁所有表 """
        # 请谨慎使用
        Base.metadata.drop_all(bind=self.engine)

    def save(self, obj: Base):
        """ 保存一条记录 """
        with self.session.begin() as session:
            session.add(obj)

    def save_all(self, objs: List[Base]):
        """ 保存一批记录 """
        with self.session.begin() as session:
            session.add(objs)

    def insert_or_update(self, obj: Base):
        """ 插入或更新一条记录 """
        with self.session.begin() as session:
            obj.update_time = datetime.utcnow()
            insert_stmt = insert(obj.__class__).values(obj.to_dict())
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(obj.to_dict())
            session.execute(on_duplicate_key_stmt)

    def get_security_info(self, code: Any, date: Any = None) -> Optional[Security]:
        """
        获取单个标的信息（股票/基金/指数的信息）
        see https://www.joinquant.com/help/api/help#JQData:%E8%8E%B7%E5%8F%96%E6%A0%87%E7%9A%84%E6%A6%82%E5%86%B5
        :param code: 证劵代码
        :param date: 获取指定日期的标的信息（默认为None, 仅支持股票）
        :return: 单个标的信息
        """
        # 避免查询不到结果而抛出异常
        try:
            # 判断是否需要使用日期
            if date is None:
                statement = select(Security).filter(Security.code == code)
            else:
                date = to_date_str(date)
                statement = select(Security).filter(Security.code == code, Security.end_date < date)
            # 执行查询语句
            security = self.session().scalars(statement).one()
            return security
        except NoResultFound as _:
            pass
        return None

    def get_all_securities(self, types: List = None, date: Any = None) -> Optional[pd.DataFrame]:
        """
        获取平台支持的所有股票、基金、指数、期货信息
        see https://www.joinquant.com/help/api/help#JQData:%E8%8E%B7%E5%8F%96%E6%A0%87%E7%9A%84%E6%A6%82%E5%86%B5
        :param types: 用来过滤标的类型,列表元素可选
        :param date:  用于获取某日期还在上市的股票信息（默认值为None, 表示获取所有日期的股票信息）
        :return: 标的信息列表 [pandas.DataFrame]格式
        """
        # 默认为None时转为空列表
        if types is None: types = list()
        # 避免查询不到结果而抛出异常
        try:
            # 判断是否需要使用日期
            if date is None:
                statement = select(Security).where(Security.security_type.in_(types))
            else:
                date = to_date_str(date)
                statement = select(Security).where(Security.security_type.in_(types), Security.end_date > date)
            # 执行查询语句
            with self.engine.connect() as conn:
                df = pd.read_sql_query(statement, conn, index_col="code")
            return df
        except NoResultFound as _:
            pass
        return None

    def get_price(self, security, start_date=None, end_date=None, count=None, frequency='daily', fields=None,
                  skip_paused=False, fill_paused=True, fq='pre',  panel=True):
        """
        1天/分钟行情数据
        see https://www.joinquant.com/help/api/help#JQData:%E9%80%9A%E7%94%A8%E8%A1%8C%E6%83%85%E6%8E%A5%E5%8F%A3
        :param security: 标的（股票、期货、基金、指数、期权）
        :param start_date: 开始时间
        :param end_date: 结束时间
        :param count: 返回的结果集的行数
        :param frequency: 单位时间长度（daily、1d、minute、1m; 3m、5d...）
        :param fields: 获取数据的字段名称（默认返回标准字段['open','close','high','low','volume','money']）
        :param skip_paused: 是否跳过不交易日期
        :param fill_paused: 对于停牌股票的价格处理
        :param fq: 复权选项（默认为pre, 前复权: pre、不复权: none、后复权: post）
        :param panel: 指定返回的数据格式为panel（默认为True, 指定panel=False时返回dataframe格式）
        :return: 行情数据
        """
        # 避免查询不到结果而抛出异常
        try:
            statement = select(Price).where(Security.code.is_(security))
            # 执行查询语句
            with self.engine.connect() as conn:
                df = pd.read_sql_query(statement, conn, index_col="code")
            return df
        except NoResultFound as _:
            pass
        return None
