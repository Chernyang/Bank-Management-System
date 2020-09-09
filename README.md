## 环境

本实验使用MySQL+Django实现，环境为Windows 10

## 配置

首先在本地创建数据库：bankdb

```shell
create database bankdb;
```

然后进入文件目录：

```shell
cd Bank_System
```

激活虚拟环境：

```shell
ll_env\Scripts\activate
```

生成数据库迁移文件及数据迁移

```shell
cd mysite
py manage.py makemigrations
py manage.py migrate
```

## 运行

```
py manage.py runserver
```

进入http://127.0.0.1:8000/bank/ 即可开始运行。
