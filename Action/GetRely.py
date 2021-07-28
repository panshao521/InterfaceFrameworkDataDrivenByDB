# -*- coding: utf-8 -*-
"""
Time:     2021/7/26 23:48
Author:   panyuangao@foxmail.com
File:     GetRely.py
Describe: 
"""
from Util.Md5_Encrypt import md5_encrypt
from Util.DbHandler import DB

class GetRely(object):
    def __init__(self):
        pass

    @classmethod
    def get(cls, req_data, rely_data, header_source = {}):
        req_flag = 0
        if isinstance(req_data, dict):
            data = req_data.copy()
        elif isinstance(req_data, str):
            data = ""
            req_flag = "str"
        db = DB()
        # 1表示依赖数据处理完毕，0表示不需要处理依赖数据,或者处理依赖数据异常
        flag = 1
        # {"response":{"查询用户博文->12":["articleId"]}}
        for key, value in rely_data.items():
            for apiname_caseid, field_list in value.items():
                api_name, case_id = apiname_caseid.split("->")
                api_id = db.get_api_id(api_name)
                store_rely_data = db.get_rely_data(api_id, int(case_id)) # 从数据库取出依赖数据
                # 例：{'request': {}, 'response': {'查询用户博文': {12: {'articleId': '47'}}}}
                print("store_rely_data:",store_rely_data)
                for field in field_list:
                    if key == "request":
                        if field in store_rely_data["request"][api_name][int(case_id)]:
                            if field == "password":
                                password = md5_encrypt(store_rely_data["request"][api_name][int(case_id)][field])
                                data[field] = password
                            elif req_flag == "str":
                                data = store_rely_data["request"][api_name][int(case_id)][field]
                            else:
                                data[field] = store_rely_data["request"][api_name][int(case_id)][field]
                            flag = 1
                        else:
                            flag = 0
                    elif key == "response":
                        if field in store_rely_data["response"][api_name][int(case_id)]:
                            if req_flag == "str":
                                data = store_rely_data["response"][api_name][int(case_id)][field]
                            else:
                                data[field] = store_rely_data["response"][api_name][int(case_id)][field]
                            flag = 1
                        else:
                            flag = 0
        return flag, data

if __name__ == "__main__":
    data_source = {"username":"", "password":""}
    # rely_data = {"request":{"用户注册->1":["username","password"]}, "response":{"用户注册->1":["code"]}}
    rely_data = {"request":{"用户注册->1":["username","password"]}, "response":{}}
    flag,data = GetRely.get(data_source, rely_data)
    print(flag,data)
