# Quant

跟坤哥真枪实弹学量化

亏钱的代码不是好代码,赚钱的代码也不一定是好代码

1. 盈利是第一要义
2. 不要受限或自我设限
3. 尊重游戏规则
4. 调研、决策、执行、接受
5. 实践是检验真理的唯一标准

## 代码模块定义

- 数据源 DataSource
  - [聚宽数据](https://www.joinquant.com/)
  - [TuShare](https://www.tushare.pro/)
- 决策类
- 回测类
- 模拟类
- 工具类 utils

## 配置环境变量

```dotenv
# 数据库配置
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USERNAME=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=quant

# 聚宽数据
JQ_USERNAME=your_phone_number
JQ_PASSWORD=your_password
```

## 环境搭建

- 创建

```shell
conda create -n Quant python=3.9
```

- 激活

```shell
conda activate Quant
```

- 安装依赖

```shell
conda install --yes --file requirements.txt
```

- 关闭

```shell
deactivate
```

- 加速(可选)

添加清华源

```shell
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/
```