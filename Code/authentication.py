#!D:\Anaconda3\python.exe
# -*- coding: utf-8 -*-
'''
# Author  : CJH
# Time    : 2019-12-13
# File    : authentication.py
# Version : 1.0.0
# Describe: 验证模块
# Update  :
'''

import requests
import urllib.error
import socket
import pymysql
import gc
import traceback
import random
from retry import retry
import configManager



class Authentication(object):
    def __init__(self):
        print('<*> 正在实例化验证模块.....')
        self.User_Agent = random.choice(configManager.User_Agent)

    @retry(tries=5, delay=2)
    def dataBaseVerify(self, dbParams):
        """
        验证数据库连接状态
        :param dbParams: 数据库连接参数
        :return: 验证通过返回 True, 否则返回 False
        """
        print("<*> 正在验证 MySQL 数据库连接状态.....")
        try:
            pymysql.connect(host=dbParams['host'],
                            port=dbParams['port'],
                            user=dbParams['user'],
                            password=dbParams['password'],
                            database=dbParams['database'],
                            charset=dbParams['charset']
                            )
            print("<+> 数据库验证通过")
            return True
        except:
            print("<-> 数据库验证失败")
            traceback.print_exc()
            return False

    @retry(tries=5, delay=2)
    def httpCodeVerify(self, url):
        """
        验证 HTTP 状态码
        :param url: 需要验证的网址
        :return: 验证通过返回 True, 否则返回 False
        """
        print("<*> 正在验证网页连接: {0}".format(url))
        try:
            headers = {'User-Agent':self.User_Agent}
            requests.get(url, headers=headers)
            print("<+> 网页连接通过")
            return True
        except urllib.error.HTTPError as e:
            print("<-> 网页连接失败")
            #print("ERROR: " + str(e) + configManager.httpStatusCode[str(e.code)])
            traceback.print_exc()
            return False

    @retry(tries=5, delay=2)
    def proxyVerify(self, url, protocol, ip, port):
        """
        验证代理 IP 是否可用
        :param url: 需要爬取的网址
        :param protocol: 代理协议
        :param ip: 代理 IP
        :param port: 代理端口
        :return: 返回验证结果
        """
        check_url = url
        proxy_url = "{0}://{1}:{2}".format(protocol, ip, port)
        print("<*> 正在验证代理 IP 可用性")
        socket_timeout = 30
        socket.setdefaulttimeout(socket_timeout)
        try:
            proxy_dict = {
                protocol: proxy_url
            }
            headers = {'User-Agent': self.User_Agent}
            response = requests.get(check_url, proxies=proxy_dict ,headers=headers)
            code = response.status_code
            if code >= 200 and code < 300:
                print("<+> 可用的代理 IP 和端口：{0}:{1}:{2}".format(protocol,ip,port))
                print("<+> 验证通过")
                return True
            else:
                print("<-> 不可用的代理 IP 和端口：{0}:{1}:{2}".format(protocol,ip,port))
                print("<-> 验证不通过")
                return False
        except:
            print("<-> 不可用的代理 IP 和端口：{0}:{1}:{2}".format(protocol,ip,port))
            traceback.print_exc()
            return False
        finally:
            gc.collect()



if __name__ == "__main__":
    import proxyPool

    MySQL = configManager.MySQLParams
    url = configManager.tender_urls['广东省政府采购网']
    # proxy = proxyPool.ProxyPool().getProxy()
    aut = Authentication()
    aut.dataBaseVerify(MySQL)
    aut.httpCodeVerify(url)
    # aut.proxyVerify(url, proxy['protocol'], proxy['ip'], proxy['port'])


