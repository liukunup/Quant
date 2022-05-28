#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author : Liu Kun
# email  : liukunup@163.com
# date   : 2022-05-23 21:43:30
# func   : 调试测试文件

from DataSource.ds_join_quant import JoinQuant


if __name__ == "__main__":
    # 聚宽数据 实例化 (*自动读取配置信息)
    ds = JoinQuant()
    # 登陆
    ds.login()
    # 以下为测试代码
    # TODO
    # 退出
    ds.logout()
