import os
from dotenv import load_dotenv


def load_env_file():
    # 使用根路径的文件夹名称来分割 再组合获取项目根路径
    root_path_name = "Quant"
    splits = os.getcwd().split(root_path_name)
    root_path = os.path.join(splits[0], root_path_name)
    env_file = os.path.join(root_path, ".env")
    if os.path.exists(env_file):
        load_dotenv(env_file)
        os.environ["IS_ENV_LOAD"] = "YES"
    else:
        print("请在项目根路径下新增.env环境变量配置文件 或 通过其他方式传入环境变量!")
    pass


def get_database_conf(debug=False):
    """
    获取环境变量里的 MYSQL数据库 配置
    :param debug: 调试打印开关
    :return: 数据库配置(dict格式)
    """
    # 检查是否已经加载过环境变量
    if os.getenv("IS_ENV_LOAD") != "YES":
        load_env_file()
    # 获取 MYSQL数据库 环境变量
    db_dict = {
        "HOST": os.getenv("MYSQL_HOST") or "127.0.0.1",
        "PORT": int(os.getenv("MYSQL_PORT")) or 3306,
        "USERNAME": os.getenv("MYSQL_USERNAME") or "root",
        "PASSWORD": os.getenv("MYSQL_PASSWORD") or "123456",
        "DATABASE": os.getenv("MYSQL_DATABASE") or "quant",
    }
    # 调试打印获取的数据库配置
    if debug:
        print(db_dict)
    return db_dict


def get_join_quant_conf(debug=False):
    """
    获取环境变量里的 聚宽数据 配置
    :param debug: 调试打印开关
    :return: 聚宽数据的配置(dict格式)
    """
    # 检查是否已经加载过环境变量
    if os.getenv("IS_ENV_LOAD") != "YES":
        load_env_file()
    # 获取 聚宽数据 环境变量
    join_quant_dict = {
        "USERNAME": os.getenv("JQ_USERNAME") or "phone",
        "PASSWORD": os.getenv("JQ_PASSWORD") or "password",
    }
    # 调试打印获取的聚宽数据平台配置
    if debug:
        print(join_quant_dict)
    return join_quant_dict
