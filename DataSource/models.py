from DataSource import Base
from sqlalchemy import Column, Integer, Float, String, DateTime, Date
from datetime import datetime


class Security(Base):
    """ 标的(股票/基金/指数等) """
    __tablename__ = "security"
    # 记录编号
    id = Column(Integer, primary_key=True)
    # 业务字段
    code = Column(String(256), comment="证券代码", nullable=False, unique=True, index=True)
    name = Column(String(256), comment="缩写简称")
    display_name = Column(String(256), comment="中文名称")
    start_date = Column(Date(), comment="上市日期")
    end_date = Column(Date(), comment="退市日期")
    security_type = Column(String(256), comment="类型(stock: 股票, index: 指数; etf: ETF基金, fja: 分级A, fjb: 分级B)")
    security_parent = Column(String(256), comment="分级基金的母基金代码")
    # 记录时间
    create_time = Column(DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = Column(DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Security(id={self.id!r}, code={self.code!r}, name={self.name!r}, display_name={self.display_name!r})"

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns if getattr(self, c.name, None)}


class Price(Base):
    """ 标的(股票/基金/指数等) """
    __tablename__ = "price"
    # 记录编号
    id = Column(Integer, primary_key=True)
    # 业务字段
    code = Column(String(256), comment="证券代码", nullable=False)
    p_time = Column(DateTime(), comment="时间戳")
    p_open = Column(Float, comment="时间段开始时价格")
    p_close = Column(Float, comment="时间段结束时价格")
    p_low = Column(Float, comment="时间段中的最低价")
    p_high = Column(Float, comment="时间段中的最高价")
    volume = Column(Float, comment="时间段中的成交的股票数量")
    money = Column(Float, comment="时间段中的成交的金额")
    factor = Column(Float, comment="复权标识")
    p_high_limit = Column(Float, comment="时间段中的涨停价")
    p_low_limit = Column(Float, comment="时间段中的跌停价")
    p_avg = Column(Float, comment="时间段中的平均价")
    p_pre_close = Column(Float, comment="前一个单位时间结束时的价格")
    paused = Column(Float, comment="是否停牌")
    open_interest = Column(Float, comment="期货(期权)持仓量")
    # 记录时间
    create_time = Column(DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = Column(DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Price(id={self.id!r}, code={self.code!r})"

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns if getattr(self, c.name, None)}
