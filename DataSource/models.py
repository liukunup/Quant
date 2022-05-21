from DataSource import Base
from sqlalchemy import Column, Integer, String, DateTime, Date
from datetime import datetime


class Security(Base):
    """ 标的(股票/基金/指数等) """
    __tablename__ = "security"
    # 记录编号
    id = Column(Integer, primary_key=True)
    # 业务字段
    code = Column(String(32), comment="证券代码", nullable=False, unique=True, index=True)
    name = Column(String(256), comment="缩写简称")
    display_name = Column(String(256), comment="中文名称")
    start_date = Column(Date(), comment="上市日期")
    end_date = Column(Date(), comment="退市日期")
    security_type = Column(String(16), comment="类型(stock: 股票, index: 指数; etf: ETF基金, fja: 分级A, fjb: 分级B)")
    security_parent = Column(String(256), comment="分级基金的母基金代码")
    # 记录时间
    create_time = Column(DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = Column(DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Security(id={self.id!r}, code={self.code!r}, name={self.name!r})"
