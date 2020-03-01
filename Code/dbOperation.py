#!D:\Anaconda3\python.exe
# -*- coding: utf-8 -*-
'''
# Author  : CJH
# Time    : 2019-12-13
# File    : dbOperation
# Version : 1.0.0
# Describe: 数据库配置与操作
# Update  :
'''

import configManager
import pymongo
import pymysql


# MySQL数据库配置和基础操作
class MysqlOperate(object):
    def __init__(self):
        """
        配置并连接数据库

        """
        print("<*> 正在配置并连接数据库")
        self.db = pymysql.connect(host=configManager.MySQLParams['host'],
                                  port=configManager.MySQLParams['port'],
                                  user=configManager.MySQLParams['user'],
                                  password=configManager.MySQLParams['password'],
                                  database=configManager.MySQLParams['database'],
                                  charset=configManager.MySQLParams['charset']
                                  )

        #self.cur = self.db.cursor()

    #
    # def execute(self, operation, *data_tuple):
    #     """
    #     操作数据库
    #     :param operation: 数据库操作指令
    #     :param data_tuple: 传入的可变参数
    #     :return: 无
    #     """
    #     self.cur.execute(operation, data_tuple)
    #
    #
    # def fetch(self):
    #     """
    #     获取数据库中的数据
    #     :return: 数据 data
    #     """
    #     data = self.cur.fetchall()
    #     return data
    #
    # def closedb(self):
    #     self.db.commit()
    #     self.cur.close()
    #     self.db.close()


# MongoDB数据库配置和基础操作
class MongoOperate(object):
    def __init__(self):
        """
        初始化数据库
        """
        print("<*> 正在配置并连接数据库.....")
        user = configManager.MongodbParams['userName']
        port = configManager.MongodbParams['port']
        collection1 = configManager.MongodbParams['collection1']
        collection2 = configManager.MongodbParams['collection2']
        collection3 = configManager.MongodbParams['collection3']
        self.client = pymongo.MongoClient(user, port)
        self.database = self.client["DIBS"]
        self.collection1 = self.database[collection1]
        self.collection2 = self.database[collection2]
        self.collection3 = self.database[collection3]


if __name__ == "__main__":
    order1 = '''
    create table tenders(datetimes varchar(16),
                        titles varchar(256),
                        budgets varchar(64),
                        deadlines varchar(32),
                        hrefs varchar(256),
                        send varchar(8))default charset=utf8MB4
    '''
    # order2 = '''
    #     create table proxy(protocol varchar(32),
    #                     ip varchar(32),
    #                     port varchar(32),
    #                     speed varchar(32))default charset=utf8MB4
    #     '''

    order3 = """
    insert into tenders values(%s,%s,%s,%s,%s,%s,%s)
    """

    order4 = """
        insert into proxy values(%s,%s,%s,%s)
        """
    order5 = "update tenders set datetimes=%s where datetimes=%s"
    db = MysqlOperate().db
    cur = db.cursor()
    # cur.execute(order1)
    a = ["广东省政府采购网","广州公共资源交易公共服务平台", "深圳市公共资源交易平台"]
    for i in a:
        cur.execute(order3, ("%s"%i,"2019-12-01 00:00","boot_up","boot_up","boot_up","boot_up","boot_up"))
    # cur.execute(order4, ("HTTP", "183.166.20.92", "9999", "0.123"))
    # cur.execute(order5, ("2019-12-15 00:00", "2019-12-01 00:00"))
    db.commit()
    cur.close()
    db.close()


    # import time
    # col1 = MongoOperate().collection1
    # col2 = MongoOperate().collection2
    # col3 = MongoOperate().collection3
    # print("<+> mongodb 初始化成功")
    # col1.insert_one({"datetimes":"2019-12-10 00:00", "href":"boot_up", "titles":"boot_up",
    #                          "budgets":"boot_up", "deadlines":"boot_up", "send":"boot_up"})
    # col1.remove({})
    # col1.update({"send": "yes"}, {"$set": {"send": "no"}})
    # time.sleep(10)
    # a = [i for i in col1.find({}, {"_id": 0})]
    # print(a)
    # last_time = col1.find({}, {"datetimes": 1, "_id": 0}).sort("datetimes", -1).limit(1)
    # print(list(last_time))

    # #col2.remove({})
    # b = [i for i in col2.find({})]
    # print(b)
    # #col3.remove({})
    # c = [i for i in col3.find({})]
    #print(c)

















