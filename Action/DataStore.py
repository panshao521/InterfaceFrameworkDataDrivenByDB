# -*- coding: utf-8 -*-
"""
Time:     2021/7/26 23:48
Author:   panyuangao@foxmail.com
File:     DataStore.py
Describe: 
"""
from Util.DbHandler import DB
import re


class RelyDataStore(object):
    def __init__(self):
        pass

    @classmethod
    def do(cls, data_store_point, api_name, case_id, req_data, res_data):
        tmp = {"request": {}, "response": {}}
        data_map = {"request": req_data, "response": res_data}
        for key, store_point in data_store_point.items():
            # data_store_point例子：{"request":["username","password"]} 或 {"response":["token","userid"]}
            # data_store_point正则例子{"response": {"articleId": "'articleId': (\d+)"}}
            if key in data_map.keys():  # 取的是被依赖接口中request或response中的参数，才做处理
                for field in store_point:
                    if field in data_map[key]:
                        val = data_map[key][field] # 从req_data或res_data中获取对应字段的值
                    elif isinstance(store_point, dict) and field in str(data_map[key]):
                        regular_exp = store_point[field] # 获取正则表达式
                        print("regular_exp:",regular_exp)
                        if re.search(regular_exp, str(data_map[key])):
                            val = re.search(regular_exp, str(data_map[key])).group(1) # 通过正则表达式获取对应字段的值
                    else:
                        val = None
                        print("字段【%s】在原始数据源req_source中不存在！" % field)

                    if val:
                        if api_name not in tmp[key]:
                            tmp[key] = {api_name: {case_id: {field: val}}}
                        elif case_id not in tmp[key][api_name]:
                            tmp[key][api_name] = {case_id: {field: val}}
                        else:
                            tmp[key][api_name][case_id][field] = val

        # 将处理好的被依赖数据存入数据中
        if tmp["request"] or tmp["response"]:
            db = DB()
            api_id = db.get_api_id(api_name)
            db.update_store_data(api_id, case_id, tmp)

    # @classmethod
    # def do1(cls, data_store_point, api_name, case_id, req_data, res_data):
    #     tmp = {"request": {}, "response": {}}
    #     for key, store_point_list in data_store_point.items():
    #         if key == "request":
    #             # 说明取的是被依赖接口请求参数中的数据
    #             for field in store_point_list:
    #                 if field in req_data:
    #                     val = req_data[field] # 获取对应字段的值
    #                     if api_name not in tmp["request"]:
    #                         tmp["request"] = {api_name: {case_id: {field: val}}}
    #                     elif case_id not in tmp["request"][api_name]:
    #                         tmp["request"][api_name] = {case_id: {field: val}}
    #                     else:
    #                         tmp["request"][api_name][case_id][field] = val
    #                 else:
    #                     print("字段【%s】在原始数据源req_source中不存在！" % field)
    #         elif key == "response":
    #             # 说明取的是被依赖接口请响应body中的数据
    #             for field in store_point_list:
    #                 if field in res_data:
    #                     val = res_data.get(field) # 获取对应字段的值
    #                     if api_name not in tmp["response"]:
    #                         tmp["response"] = {api_name: {case_id: {field: val}}}
    #                     elif case_id not in tmp["response"][api_name]:
    #                         tmp["response"][api_name] = {case_id: {field: val}}
    #                     else:
    #                         tmp["response"][api_name][case_id][field] = val
    #                 else:
    #                     print("字段【%s】在原始数据源res_source中不存在！" % field)
    #
    #     # 将处理好的被依赖数据存入数据中
    #     if tmp["request"] or tmp["response"]:
    #         db = DB()
    #         api_id = db.get_api_id(api_name)
    #         db.update_store_data(api_id, case_id, tmp)

