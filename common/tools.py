import re
from common.handle_conf import conf
#
# def replace_data(data, cls):
#     """
#     替换数据
#     :param data: 要进行替换的用例数据(字符串)
#     :param cls: 测试类
#     :return:
#     """
#     while re.search('#(.+?)#', data):
#         res2 = re.search('#(.+?)#', data)
#         item = res2.group()
#         attr = res2.group(1)
#         value = getattr(cls, attr)
#         # 进行替换
#         data = data.replace(item, str(value))
#
#     return data

# --------------升级版  替换数据同时可以去找测试类和配置文件中的数据--------------------
def replace_data(data, cls):
    """
    替换数据
    :param data: 要进行替换的用例数据(字符串)
    :param cls: 测试类
    :return:
    """
    while re.search('#(.+?)#', data):
        res2 = re.search('#(.+?)#', data)
        item = res2.group()
        attr = res2.group(1)
        try:
            value = getattr(cls, attr)
        except AttributeError:
            value = conf.get('test_data',attr)
        # 进行替换
        data = data.replace(item, str(value))

    return data
