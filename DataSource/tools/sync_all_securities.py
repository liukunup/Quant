#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author : Liu Kun
# email  : liukunup@163.com
# date   : 2022-05-22 16:27:30
# func   : 同步所有标的信息到本地数据库

from DataSource.ds_join_quant import JoinQuant


if __name__ == "__main__":
    # 聚宽数据 实例化 (*自动读取配置信息)
    ds = JoinQuant()
    # 1. 登陆
    ds.login()
    # 2. 逐类别获取标的信息
    type_list = ["stock", "fund", "index", "futures", "options", "etf", "lof", "fja", "fjb", "open_fund", "bond_fund",
                 "stock_fund", "QDII_fund", "money_market_fund", "mixture_fund"]
    for item in type_list:
        print("-" * 50, item, "-" * 50)
        ds.get_all_securities(types=[item], date=None)
    # 3. 打印消耗情况
    print(f"今日已用 {ds.get_usage_count()} 条.")
    # 4. 退出
    ds.logout()
