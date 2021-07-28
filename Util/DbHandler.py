# -*- coding: utf-8 -*-
"""
Time:     2021/7/26 23:34
Author:   panyuangao@foxmail.com
File:     DbHandler.py
Describe: 
"""
import pymysql
from datetime import datetime
from Config.ProjConfigVar import db_config_path
from Util.ConfigHandler import ConfigParse

class DB(object):
    def __init__(self):
        # 获取数据库配置信息
        self.db_config = ConfigParse.get_db_config(db_config_path)
        # 连接数据库，创建数据数据库连接
        self.conn = pymysql.connect(
            host = self.db_config.get("host"),
            port = self.db_config.get("port"),
            user = self.db_config.get("user"),
            password = self.db_config.get("password"),
            database = self.db_config.get("db"),
            charset = self.db_config.get("utf8"),
        )
        # 获取数据库连接对象，获取操作数据表的游标对象
        self.cur = self.conn.cursor()

    def db_conn(self):
        try:
            pass
        except:
            pass

    def close_connect(self): # 关闭数据库连接
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_api_list(self):
        sqlStr = "SELECT * FROM interface_api WHERE STATUS = 1"
        self.cur.execute(sqlStr)
        data = self.cur.fetchall()
        apiList = list(data)
        return apiList

    def get_api_id(self, api_name):
        sqlStr = "select api_id from interface_api where api_name='%s'" %api_name
        self.cur.execute(sqlStr)
        api_id = self.cur.fetchall()[0][0]
        return api_id

    def get_api_case(self, api_id):
        sqlStr = "select * from interface_test_case where api_id=%s and status=1" %api_id
        self.cur.execute(sqlStr)
        api_case_list = list(self.cur.fetchall())
        return api_case_list

    def get_rely_data(self, api_id, case_id):
        sqlStr = "select data_store from interface_data_store where api_id=%s and case_id=%s" %(api_id, case_id)
        self.cur.execute(sqlStr)
        rely_data = eval(self.cur.fetchall()[0][0])
        return rely_data

    def write_check_result(self, case_id, errorInfo, res_data):
        sqlStr = "update interface_test_case set error_info=\"%s\", res_data=\"%s\", ctime=\"%s\" where id=%s" %(errorInfo, res_data, datetime.now(),case_id)
        print(sqlStr)
        self.cur.execute(sqlStr)
        self.conn.commit()

    def update_store_data(self, api_id, case_id, store_data):
        sqlStr = "select data_store from interface_data_store where api_id=%s and case_id=%s" %(api_id, case_id)
        self.cur.execute(sqlStr)
        if self.cur.fetchall():
            sqlStr = "update interface_data_store set data_store=\"%s\" where api_id=%s and case_id=%s" %(store_data, api_id, case_id)
            self.cur.execute(sqlStr)
            self.conn.commit()
        else:
            sqlStr = "insert into interface_data_store values(%s, %s, \"%s\", '%s')" %(api_id, case_id, store_data, datetime.now())
            self.cur.execute(sqlStr)
            self.conn.commit()

if __name__ == '__main__':
    db = DB()
    # print(db.get_api_list())
    # print(db.get_api_id("用户注册"))
    print(db.get_rely_data(1,1))
