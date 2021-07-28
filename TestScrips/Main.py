# -*- coding: utf-8 -*-
"""
Time:     2021/7/26 23:53
Author:   panyuangao@foxmail.com
File:     Main.py
Describe: 
"""
from Util.DbHandler import  DB
from Util.HttpClient import HttpClient
from Action.GetRely import *
from Action.DataStore import RelyDataStore
from Action.CheckResult import CheckResult
from Util.Log import *


def main():
    # 第一步：连接数据库，获取接口测试相关数据库
    # 第二步：处理数据依赖
    # 第三步：发送接口请求，执行接口测试用例，并获取响应body
    # 第四步：处理数据依赖存储
    # 第五步：结果校验
    # 第六步：日志收集、整理并展示

    db = DB()  # 创建连接数据库的实例对象
    api_list = db.get_api_list()  # 从数据库中获取需要执行的api集合
    for id, api in enumerate(api_list, 1):
        api_id = api[0]
        api_name = api[1]
        req_url = api[2]
        req_method = api[3]
        parm_type = api[4]
        print(api_id, api_name,req_url,req_method,parm_type)
        # 通过api_id 获取它对应的测试用例数据集
        api_case_list = db.get_api_case(api_id)
        # print("api_case_list:",api_case_list)
        # 遍历测试用例
        for idx, case in enumerate(api_case_list, 1):
            case_id = case[0]
            req_data = eval(case[2]) if case[2] else {} # 请求数据的格式
            rely_data = eval(case[3]) if case[3] else {} # 当前用例依赖的数据格式
            protoclo_code = case[4] # 接口期望响应code
            data_store_point = eval(case[6]) if case[6] else {} # 依赖数据存储格式
            check_point = eval(case[7]) if case[7] else {} # 接口响应校验依据数据
            falg = -1 # -1表示不需要数据依赖，1表示数据依赖处理成功，0表示数据依赖处理失败

            # 第二步：处理数据依赖
            if rely_data:
                flag, req_data = GetRely.get(req_data, rely_data)
            else:
                info("接口【%s】的第%s条用例不需要依赖数据" % (api_name, idx))

            # 第三步：发送接口请求，执行接口测试用例，并获取响应body
            print("req_data :", req_data)
            if falg == 0:
                info("依赖数据未正确替换")
                continue
            hc = HttpClient()
            responseObj = hc.request(req_url,req_method,parm_type,req_data)
            prot_code = responseObj.status_code

            # 第四步：处理数据依赖存储
            if prot_code == protoclo_code:
                # 说明接口是正常响应的
                res_data = responseObj.json()
                if data_store_point:
                    RelyDataStore.do(data_store_point,api_name,case_id,req_data,res_data ) # 存储依赖数据

                # 第五步：结果校验
                print("res_data :",res_data )
                print("check_point:",check_point)
                error_info = CheckResult.check(res_data ,check_point)

                # 第六步：日志收集、整理并展示
                if error_info:
                    db.write_check_result(case_id,error_info,req_data)
                else:
                    db.write_check_result(case_id, "", req_data)

            else:
                info("接口【%s】的用例编号为%s的用例的响应协议code=%s，不符合预期code=%s" %(api_name,case_id,prot_code,protoclo_code))

if __name__ == '__main__':
    main()
