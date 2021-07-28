# -*- coding: utf-8 -*-
"""
Time:     2021/7/26 23:35
Author:   panyuangao@foxmail.com
File:     ConfigHandler.py
Describe: 
"""
from  configparser import ConfigParser

class ConfigParse(object):
    def __init__(self):
        pass

    @classmethod
    def get_db_config(cls, configPath):
        cf = ConfigParser() # ConfigParser是一个python类，创建该类方法的实例对象
        cf.read(configPath)
        host = cf.get("mysqlconf", "host")
        port = int(cf.get("mysqlconf", "port")) # 数据库连接端口号需要的是int类型
        user = cf.get("mysqlconf", "user")
        password = cf.get("mysqlconf", "password")
        db = cf.get("mysqlconf", "db_name")
        return {"host":host, "port":port, "user":user, "password":password, "db":db}


if __name__ == '__main__':
    from Config.ProjConfigVar import db_config_path
    res = ConfigParse.get_db_config(db_config_path)
    print(res)