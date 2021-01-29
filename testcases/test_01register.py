# -*- coding:utf-8 -*-
# @Time   : 2021/1/17 23:31
# @Author :sleep
# @Email  :1285592010@qq.com
# @File   : test_01register.py
# @Software:PyCharm
# @Translate:
# -*- coding:utf-8 -*-
# @Time   : 2021/1/17 22:21
# @Author :sleep
# @Email  :1285592010@qq.com
# @File   : test_01login.py
# @Software:PyCharm
# @Translate:
import unittest
import os
import requests
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handler_log import my_log


@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlsx"), "register")
    # 读取用例数据
    cases = excel.read_data()
    # 项目的基本地址
    base_url = conf.get("env", "base_url")
    # 请求头，登录不需要
    # base_url = conf.get('env', 'base_url')

    @list_data(cases)
    def test_register(self, item):
        # 第一步：准备用例数据
        # 1）接口地址
        url = self.base_url + item["url"]
        # 2）接口请求参数
        params = eval(item["data"])
        # 3）获取请求方法
        method = item["method"].lower()
        # 4）用例预期结果
        expected = eval(item["expected"])

        # 第二步：请求接口，获取返回实际参数
        response=requests.request(method,url,json=params)
        res = response.json()
        # 第三步：断言
        try:
            # self.assertEqual(expected['code'], res['code'])
            self.assertDictIn(expected,res)
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
