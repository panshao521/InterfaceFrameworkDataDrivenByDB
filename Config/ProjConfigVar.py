# -*- coding: utf-8 -*-
"""
Time:     2021/7/26 23:36
Author:   panyuangao@foxmail.com
File:     ProjConfigVar.py
Describe: 
"""
import os

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 项目目录路径

db_config_path = os.path.join(proj_path,"Config", "db_config.ini") # 数据库地址配置文件路径
log_conf_path = os.path.join(proj_path,"config","Logger.conf") # log配置文件路径

# 依赖数据存储公共变量
REQUEST_DATA = {} # request data
RESPONSE_DATA = {} # response data