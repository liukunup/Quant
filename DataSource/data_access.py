#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author : Liu Kun
# email  : liukunup@163.com
# date   : 2022-05-21 12:00:00
# source : 本地 数据库接入层

from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from DataSource import Base
from DataSource.models import Security


class LocalDatabaseServer:

    def __init__(self, host, port, username, password, database):
        self.engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")
        self.session = sessionmaker(bind=self.engine)

    def create_all(self):
        """ 创建所有表 """
        Base.metadata.create_all(bind=self.engine)

    def destroy_all(self):
        """ 销毁所有表 """
        Base.metadata.drop_all(bind=self.engine)

    def save(self, obj: Base):
        session = self.session()
        session.add(obj)
        session.commit()

    def save_all(self, objs: List[Base]):
        session = self.session()
        session.add_all(objs)
        session.commit()

    def get_security_by_code(self, code):
        try:
            session = self.session()
            security = session.query(Security).filter(Security.code == code).one()
            return security
        except NoResultFound as e:
            print(e)
        return None
