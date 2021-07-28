# -*- coding: utf-8 -*-
"""
Time:     2021/7/26 23:33
Author:   panyuangao@foxmail.com
File:     HttpClient.py
Describe: 
"""
import requests
import json


class HttpClient(object):
    def __init__(self):
        pass

    def request(self, reqUrl, reqMethod, paramsType,reqData=None,headers=None,cookies = None):
        """
        处理所有http请求，包括post、get等
        :param reqUrl:请求url
        :param reqMethod:请求方式：post、get等
        :param paramsType:参数类型,from,json,url
        :param reqData:请求体，请求入参
        :param headers:
        :param cookie:
        :return:
        """
        reqMethod = reqMethod.strip()
        paramsType = paramsType.strip()
        if reqMethod.lower() == "post":
            if paramsType == "form":
                reqData = json.dumps(reqData)
                response = self.__post(reqUrl,data=reqData,headers=headers, cookies=cookies)
                return response
            elif paramsType == "json":
                response = self.__post(reqUrl, json=reqData, headers=headers, cookies=cookies)
                return response
        elif reqMethod.lower() == "get":
            if paramsType == "url":
                # 说明是将参数直接拼接到URL
                reqUrl = "{}{}".format(reqUrl,reqData)
                print("get请求方式：",reqUrl)
                response = self.__get(reqUrl, headers=headers, cookies=cookies)
                return response
            elif paramsType == "params":
                response = self.__get(reqUrl,reqData, headers=headers, cookies=cookies)
                return response
        elif reqMethod.lower() == "put":
            if paramsType == "form":
                reqData = json.dumps(reqData)
                response = self.__put(reqUrl,data=reqData,headers=headers, cookies=cookies)
                return response
            elif paramsType == "json":
                response = self.__put(reqUrl, json=reqData, headers=headers, cookies=cookies)
                return response
        else:
            print("没有命中get、post、put")

    def __post(self, url, data=None,json= None,headers=None,cookies = None):
        #处理post类型中各种情况的情求
        response = requests.post(url, data=data,json= json,headers=headers,cookies=cookies)
        return response

    def __get(self, url, params=None, headers=None, cookies=None):
        response = requests.get(url, params=params,headers=headers, cookies=cookies)
        return response

    def __put(self, url, data=None,json= None,headers=None,cookies = None):
        #处理put类型中各种情况的情求
        response = requests.put(url, data=data,json= json,headers=headers,cookies=cookies)
        return response

if __name__ == '__main__':
    req_url, req_method, parm_type, req_data = "http://39.100.104.214:8080/getBlogContent/", "get", "url", 58
    hc = HttpClient()
    hc.request(req_url, req_method, parm_type, req_data)