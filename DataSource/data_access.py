#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author : Liu Kun
# email  : liukunup@163.com
# date   : 2022-05-21 12:00:00
# source : 本地 数据库接入层
# see https://docs.sqlalchemy.org/en/14/index.html#

from typing import Optional, List, AnyStr

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from DataSource import Base
from DataSource.models import Security


class LocalDatabaseServer:

    def __init__(self, host, port, username, password, database):
        self.engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}", future=True)
        self.session = sessionmaker(bind=self.engine, future=True)

    def create_all(self):
        """ 创建所有表 """
        Base.metadata.create_all(bind=self.engine)

    def destroy_all(self):
        """ 销毁所有表 """
        Base.metadata.drop_all(bind=self.engine)

    def save(self, obj: Base):
        """ 保存一条记录 """
        with self.session.begin() as session:
            session.add(obj)

    def save_all(self, objs: List[Base]):
        """ 保存一批记录 """
        with self.session.begin() as session:
            session.add(objs)

    def get_security_by_code(self, code: AnyStr) -> Optional[Security]:
        """
        获取单个标的信息
        :param code: 证劵代码
        :return: 单个标的信息
        """
        try:
            statement = select(Security).filter(Security.code == code)
            security = self.session().scalars(statement).one()
            return security
        except NoResultFound as _:
            pass
        return None
