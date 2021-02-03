# -*- coding:utf-8 -*-
# @Time   : 2021/1/18 11:09
# @Author :sleep
# @Email  :1285592010@qq.com
# @File   : test_03NB_update_password.py
# @Software:PyCharm
# @File name Translation:修改密码现在没做，开发是直接删除后在添加
import unittest
import os
import requests
import time
from jsonpath import jsonpath
from unittestreport import ddt,list_data
from common.handle_path import DATA_DIR
from common.handle_excel import HandleExcel
from common.handle_conf import conf
from common.handler_log import my_log
@ddt
class TestNBupdatePassword(unittest.TestCase):
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
    excel=HandleExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"03_nb_update_password_01")
    #读取用例数据
    cases=excel.read_data()
    #项目的基本地址
    base_url=conf.get("env","base_url")
    #---------------------门锁授权信息------------------------------------
    #门锁IMEI
    IMEI=conf.get("lock","imei")
    #门锁授权开始和结束时间
    ##所有开锁授权开始时间
    start_time=conf.get("time","startTime")
    end_time=conf.get("time","endTime180d")
    #实际门锁类型获取
    practical_lock_type=eval(conf.get("lock","lock_type"))
    @list_data(cases)
    def test_nb_update_password(self,item):
        #门锁类型获取
        lock_type=item["lock_type"]
        if lock_type<=self.practical_lock_type:
            #第一步：准备用例数据
            #1)获取请求接口地址
            url=self.base_url+item["url"]
            #2)请求接口参数
            #替换参数IMEI
            if '#IMEI#' in item['data']:
                imei = self.IMEI
                item['data'] = item['data'].replace('#IMEI#',imei)
            #替换参数开始和结束时间
            if "#start_time#" in item["data"]:
                start_time=self.start_time
                item["data"] = item["data"].replace("#start_time#",start_time)
            if "#end_time#" in item["data"]:
                end_time=self.end_time
                item["data"] = item["data"].replace("#end_time#",end_time)
            #替换修改密码需要的ID
            if "#userId#" in item["data"]:
                userId=self.userId
                item["data"] = item["data"].replace("#userId#",userId)
            if "#usePwId#" in item["data"]:
                usePwId=self.usePwId
                item["data"] = item["data"].replace("#usePwId#",usePwId)
            parms=eval(item["data"])
            print("请求参数",parms)
            #3）请求头
            #类级别前置以获取
            #4）获取请求方法
            method=item["method"].lower()
            #5)用例预期结果
            expected=eval(item["expected"])
            #第二步：请求接口，获取返回实际参数
            response=requests.request(method,url=url,json=parms,headers=self.token)
            res=response.json()
            print("返回数据",res)
            if item["url"]=="/userAuthorize/add":
                TestNBupdatePassword.userId=jsonpath(res,"$..userId")[0]
                TestNBupdatePassword.usePwId=jsonpath(res,"$..usePwId")[0]
            #第三部：断言
            try:
                self.assertDictIn(expected, res)
                # 成员断言，因为返回的字段不确定性，提取关键字段
            except AssertionError as e:
                # 记录日志
                my_log.error("用例--【{}】---执行失败".format(item['title']))
                # my_log.error(e)
                # 输出日志用这个方法，输出的日志比较详细点
                my_log.exception(e)
                raise e
            else:
                my_log.info("用例--【{}】---执行通过".format(item['title']))
                # 通过门锁类型，来预期录入所耗时间
                if item["lock_type"] == 3:
                    print("请激活门锁，录入开锁信息,45s")
                    time.sleep(45)
                    print("等待结束")
                if item["lock_type"] == 1 or item["lock_type"] == 2:
                    print("请激活门锁，录入开锁信息,30s")
                    time.sleep(20)
                    print("等待结束")

        else:
            my_log.info("用例--【{}】---无需执行".format(item['title']))
    def assertDictIn(self, expected, res):
        for k, v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected, res))
