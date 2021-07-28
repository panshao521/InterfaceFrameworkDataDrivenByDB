# -*- coding: utf-8 -*-
"""
Time:     2021/7/22 23:00
Author:   panyuangao@foxmail.com
File:     Log.py
Describe: 
"""
import logging.config
import logging
from Config.ProjConfigVar import log_conf_path

logging.config.fileConfig(log_conf_path)  #写绝对路径和相对路径都可以
logger = logging.getLogger("example02")

#日志配置文件：多个logger,每个logger，指定不同的handler
#handler:设定了日志输出行的格式
#handler:以及设定写日志到文件（是否回滚）？还是到屏幕
#handler：还定了打印日志的级别。

def debug(message):
    # 打印debug级别的日志方法
   logger.debug(message)

def warning(message):
    # 打印warning级别的日志方法
    logger.warning(message)

def info(message):
    # 打印info级别的日志方法
    logger.info(message)

def error(message):
    # 打印error级别的日志方法
    logger.error(message)


if __name__=="__main__":
    debug("hi")
    info("gloryroad")
    warning("hello")
    error("这是一个error日志")