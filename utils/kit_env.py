import os
from dotenv import load_dotenv


def get_database_conf(debug=False):
    """
    获取环境变量里的MYSQL数据库配置信息
    :param debug: 调试打印开关
    :return: 数据库配置(dict格式)
    """
    # 通过.env加载环境变量
    path = os.path.join(os.path.dirname(__file__), "../.env")
    if os.path.exists(path):
        load_dotenv(path)
    # 当然,也可能通过其他方式已经加载了
    db_dict = {
        "HOST": os.getenv("MYSQL_HOST") or "127.0.0.1",
        "PORT": int(os.getenv("MYSQL_PORT")) or 3306,
        "USERNAME": os.getenv("MYSQL_USERNAME") or "root",
        "PASSWORD": os.getenv("MYSQL_PASSWORD") or "123456",
        "DATABASE": os.getenv("MYSQL_DATABASE") or "quant"
    }
    # 调试打印获取的数据库配置
    if debug:
        print(db_dict)
    return db_dict
