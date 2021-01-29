# -*- coding:utf-8 -*-
# @Time   : 2021/1/20 14:56
# @Author :sleep
# @Email  :1285592010@qq.com
# @File   : test_06NB_grant_column_list.py
# @Software:PyCharm
# @File name Translation:授权列表
import unittest
import os
import requests
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_path import DATA_DIR
from common.handle_excel import HandleExcel
from common.handle_conf import conf
from common.handler_log import my_log

@ddt
class TestNBGrantColumnList(unittest.TestCase):
    #____________________类级别前置获token____________________
    @classmethod
    def setUpClass(cls) -> None:
        #1、准备登录数据
        url=conf.get("env","base_url")+"/auth/login"
        params={"username":conf.get("test_data","username"),
                "password":conf.get("test_data","password")}
        #2、请求登录接口
        response=requests.post(url=url,json=params)
        res=response.json()
        #3、提取token，放到请求头中，给后面的用例使用
        token=jsonpath(res,"$..token")[0]
        headers={"token":""}
        headers['token']=token
        cls.token=headers
    #---------------------------------------------------

    excel=HandleExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"06_nb_grant_column_list")
    #读取用例数据
    cases=excel.read_data()
    #项目的基本地址
    base_url=conf.get("env","base_url")
    #---------------------门锁授权信息------------------------------------
    #门锁IMEI
    IMEI=conf.get("lock","imei")

    @list_data(cases)
    def test_nb_grant_column_list(self,item):
        #第一步：准备用例数据
        #1)获取请求接口地址
        url=self.base_url+item["url"]
        #2)请求接口参数
        #替换参数IMEI
        if '#IMEI#' in item['data']:
            imei = self.IMEI
            item['data'] = item['data'].replace('#IMEI#',imei)
        parms=eval(item["data"])
        #3）请求头
        #类级别前置以获取
        #4）获取请求方法
        method=item["method"].lower()
        #5)用例预期结果
        expected=eval(item["expected"])
        #第二步：请求接口，获取返回实际参数
        response=requests.request(method,url=url,json=parms,headers=self.token)
        res=response.json()
        #第三部：断言
        try:
            self.assertDictIn(expected, res)
            # 成员断言，因为返回的字段不确定性，提取关键字段
        except AssertionError as e:
            # 记录日志
            my_log.error("用例--【{}】---执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.info("用例--【{}】---执行通过".format(item['title']))

    def assertDictIn(self, expected, res):
        """字典成员运算的逻辑"""
        for k, v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected, res))
