import unittest
from unittestreport import TestRunner
from common.handle_path import CASES_DIR, REPORT_DIR


def main():
    """程序的入口函数"""
    suite = unittest.defaultTestLoader.discover(CASES_DIR)
    runner = TestRunner(suite,
                        filename="锁管平台测试报告.html",
                        report_dir=REPORT_DIR,
                        tester='李谱',
                        title='锁管测试报告v1'
                        )

    runner.run()

    #  &&&&&&&&&&&&&&&&&&&&&&将测试结果发生到邮箱&&&&&&&&&&&&&&&&&&&
    # runner.send_email(host='smtp.qq.com',
    #                   port=465,
    #                   user='musen_nmb@qq.com',
    #                   password='algmmzptupjccbab',
    #                   to_addrs='3247119728@qq.com',
    #                   # to_addrs=['3247119728@qq.com','970300292@qq.com','448412893@qq.com','1363373200@qq.com','1540348104@qq.com'],
    #                   is_file=True)

    # #########################测试结果推送到钉钉群组#################################
    # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=362b478a12125d202ecb95037fdab29c130bd80c32b59'
    # runner.dingtalk_notice(url=webhook,key='测试')

    #  企业微信通知-----参照  企业微信官方的API平台--------


#  ------------扩展自定义邮件的标题和内容-------------
# from unittestreport.core.sendEmail import SendEmail

# em = SendEmail(host='smtp.qq.com',
#                port=465,
#                user='musen_nmb@qq.com',
#                password='algmmzptupjccbab')
# em.send_email(subject="测试报告", content='邮件内容', filename=None, to_addrs='3247119728@qq.com')
# ------------------------------------------------


if __name__ == '__main__':
    main()

"""
扩展知识讲解：
一、测试结果的推送
    1、通过邮件发生到相关人员邮箱
    2、推送测试结果到钉钉群


二、



"""
