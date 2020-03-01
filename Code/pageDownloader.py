#!D:\Anaconda3\python.exe
# -*- coding: utf-8 -*-
'''
# Author  : CJH
# Time    : 2019-12-13
# File    : pageDownloader.py
# Version : 1.0.0
# Describe: 网页下载器
# Update  : 代理问题有待解决, 下载的网页的时间问题，关键词筛选问题
'''
from selenium import webdriver
import time
import traceback
import configManager
from proxyPool import ProxyPool
from pageResolver import PageResolver
from dataClean import DataClean
from dataStore import DataStore


class PageDownloader(object):
    def __init__(self):
        print("<+> 正在实例化网页下载器.....")


    def downloadGDSZFCGW(self):
        """
        下载网页
        :param browser: 浏览器实例
        :return: 下载成功返回 True，失败返回 False
        """
        print("<*> 正在下载广东省政府采购网网页信息.....")
        try:
            # 解析网页
            resolved_data, update_flag = PageResolver().resovleGDSZFCGW()

            # 判断是否有合适的内容更新
            if update_flag:
                # 清洗数据
                cleaned_data = DataClean().cleanGDSZFCGW(resolved_data)
                # 存储数据
                DataStore().storeGDSZFCGW(cleaned_data)
                print("<+> 网页信息下载成功，且内容合适")
                return update_flag
            else:
                print("<+> 网页信息下载成功，但内容不合适")
                return update_flag


        except:
            print("<-> 网页信息下载失败")
            traceback.print_exc()
            return False

    def downloadGZGGZYJYGGFWPT(self):
        """
        下载网页
        :param browser: 浏览器实例
        :return: 下载成功返回 True，失败返回 False
        """
        print("<*> 正在下载广州公共资源交易公共服务平台网页信息.....")
        try:
            # 解析网页
            resolved_data, update_flag = PageResolver().resovleGZGGZYJYGGFWPT()

            # 判断是否有合适的内容更新
            if update_flag:
                # 清洗数据
                cleaned_data = DataClean().cleanGZGGZYJYGGFWPT(resolved_data)
                # 存储数据
                DataStore().storeGZGGZYJYGGFWPT(cleaned_data)
                print("<+> 广州公共资源交易公共服务平台网页信息下载成功，且内容合适")
                return update_flag
            else:
                print("<+> 广州公共资源交易公共服务平台网页信息下载成功，但内容不合适")
                return update_flag


        except:
            print("<-> 广州公共资源交易公共服务平台网页信息下载失败")
            traceback.print_exc()
            return False

    def downloadSZSGGZYJYPT(self):
        """
                下载网页
                :param browser: 浏览器实例
                :return: 下载成功返回 True，失败返回 False
                """
        print("<*> 正在下载网页信息.....")
        try:
            # 解析网页
            resolved_data, update_flag = PageResolver().resovleSZSGGZYJYPT()

            # 判断是否有合适的内容更新
            if update_flag:
                # 清洗数据
                cleaned_data = DataClean().cleanSZSGGZYJYPT(resolved_data)
                # 存储数据
                DataStore().storeSZSGGZYJYPT(cleaned_data)
                print("<+> 深圳市公共资源交易平台网页信息下载成功，且内容合适")
                return update_flag
            else:
                print("<+> 深圳市公共资源交易平台网页信息下载成功，但内容不合适")
                return update_flag


        except:
            print("<-> 深圳市公共资源交易平台网页信息下载失败")
            traceback.print_exc()
            return False



if __name__ == "__main__":
    downloaer = PageDownloader()
    for i in range(3):
        downloaer.downloadGDSZFCGW()
        downloaer.downloadGZGGZYJYGGFWPT()
        # downloaer.downloadSZSGGZYJYPT()















