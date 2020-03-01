#!D:\Anaconda3\python.exe
# -*- coding: utf-8 -*-
'''
# Author  : CJH
# Time    : 2019/12/15 16:51
# File    : scheduleEngine.py
# Version : 1.0
# Describe: 调度引擎
# Update  :
'''

import random
import time
import datetime
import os
import sys
import gc
from retry import retry

import configManager # 配置管理器
import crawlerLog # 爬虫日志
from proxyPool import ProxyPool # 代理池模块
from authentication import Authentication # 验证模块
from pageDownloader import PageDownloader # 网页下载器
from dataPusher import DataPusher # 数据推送






###### 全局变量 #######
# 动态请求报头
USER_AGENT = {
    "User-Agent":random.choice(configManager.User_Agent)
}
# URL 列表
URL_LIST = configManager.tender_urls

# 有效的 URL
VALID_URL = []
# 有效的 URL 和对应代理
VALID_URL_PROXY = {}

# 全局逻辑控制器
RESPONSE_READY = False
EXECUTE_READY = False
PUSH_READY = False
TOTAL_PUSH_READY = False
PUSH_DONE = False


# 获取当前执行的文件名
CURRENT_PY = os.path.basename(sys.argv[0]).split('.')[0]
# 创建日志对象
LOG = crawlerLog.CrawlerLog(CURRENT_PY)

######## 引擎函数 #########
@retry(tries=5, delay=2)
def authentication_engine():
    """
    验证引擎，包含三部分，分别是验证网页连接，验证代理，验证数据库
    :return: 通过验证后，赋值给响应准备标志RESPONSE_READY=True
    """
    LOG.info("<*> 开始执行验证引擎.....")
    auth = Authentication()
    global VALID_URL
    global EXECUTE_READY
    # 验证网页链接
    try:
        #### 验证网页连接 ####
        # 遍历 url 列表进行 http验证请求，将有效的 url 存储在 VALID_URL 中
        LOG.info("<*> 开始验证 HTTP 连接.....")
        for url in URL_LIST.values():
            if auth.httpCodeVerify(url):
                VALID_URL.append(url)
                EXECUTE_READY = True
                LOG.info("<+> HTTP 验证成功")
            else:
                EXECUTE_READY = False
                LOG.info("<-> HTTP 验证失败")
        EXECUTE_READY = True
    except Exception as e:
        EXECUTE_READY = False
        LOG.error("<-> HTTP 验证失败: {0}".format(str(e))) # 写入日志

    # 验证代理
    try:
        #### 验证代理 ####
        LOG.info("<*> 开始验证代理.....")
        global VALID_URL_PROXY
        # 遍历有效的 URL
        for url in VALID_URL:
            proxy = ProxyPool().getProxy()
            if auth.proxyVerify(url, proxy[0], proxy[1], proxy[2]):
                VALID_URL_PROXY[url] = proxy
                EXECUTE_READY = True
                LOG.info("<+> 验证代理成功")
            else:
                EXECUTE_READY = False
                LOG.info("<-> 验证代理失败")
            # 每进行一次 url 的代理验证，释放一次内存
            gc.collect()
    except Exception as e:
        LOG.error("<-> 代理验证失败: {0}".format(str(e)))
        EXECUTE_READY = False

    # 验证数据库
    try:
        LOG.info("<*> 开始验证数据库.....")
        mysql_params = configManager.MySQLParams
        if auth.dataBaseVerify(mysql_params):
            EXECUTE_READY = True
            LOG.info("<+> 数据库验证成功")
        else:
            LOG.info("<-> 数据库验证失败")
            EXECUTE_READY = False
    except Exception as e:
        LOG.error("<-> 数据库验证失败: {0}".format(str(e)))
        EXECUTE_READY = False

@retry(tries=5, delay=2)
def page_engine():
    LOG.info("<*> 正在启动页面下载引擎.....")
    global TOTAL_PUSH_READY
    GDSZFCGW_update_flag = False
    GZGGZYJYGGFWPT_update_flag = False
    SZSGGZYJYPT_update_flag = False
    downloaer = PageDownloader()

    # 广东省政府采购网
    try:
        GDSZFCGW_update_flag = downloaer.downloadGDSZFCGW()
        if GDSZFCGW_update_flag:
            LOG.info("<+> 广东省政府采购网页面下载成功，且内容合适")
        else:
            LOG.info("<-> 广东省政府采购网页面下载成功，但内容不合适")
    except Exception as e:
        LOG.error("<-> 广东省政府采购网页面下载失败: {0}".format(str(e)))  # 写入日志

    # 广州公共资源交易公共服务平台
    try:
        GZGGZYJYGGFWPT_update_flag = downloaer.downloadGZGGZYJYGGFWPT()
        if GZGGZYJYGGFWPT_update_flag:
            LOG.info("<+> 广州公共资源交易公共服务平台页面下载成功，且内容合适")
        else:
            LOG.info("<-> 广州公共资源交易公共服务平台页面下载成功，但内容不合适")
    except Exception as e:
        LOG.error("<-> 广州公共资源交易公共服务平台页面下载失败: {0}".format(str(e)))  # 写入日志

    # 深圳市公共资源交易平台
    # try:
    #     SZSGGZYJYPT_update_flag = downloaer.downloadSZSGGZYJYPT(downloaer.browser)
    #     if SZSGGZYJYPT_update_flag:
    #         LOG.info("<+> 深圳市公共资源交易平台页面下载成功，且内容合适")
    #     else:
    #         LOG.info("<-> 深圳市公共资源交易平台页面下载成功，但内容不合适")
    # except Exception as e:
    #     LOG.error("<-> 深圳市公共资源交易平台页面下载失败: {0}".format(str(e)))  # 写入日志


    TOTAL_PUSH_READY = GDSZFCGW_update_flag or GZGGZYJYGGFWPT_update_flag or SZSGGZYJYPT_update_flag

@retry(tries=5, delay=2)
def push_engine():
    """
    消息推送引擎
    :return: PUSH_DONE
    """
    global PUSH_DONE
    try:
        pusher = DataPusher()
        mail_text, mail_table, attachment_path = pusher.writeMail()
        pusher.sendMail(mail_text, mail_table, attachment_path)
        PUSH_DONE = True
        LOG.info("<+> 消息推送成功")

    except Exception as e:
        PUSH_DONE = False
        LOG.error("<-> 消息推送失败: {0}".format(str(e)))  # 写入日志


######### 主函数 ########
def main():
    print("-" * 40)
    print("<*> 开始执行爬虫程序.....")
    print("<*> 版本：1.0.0")
    print("-" * 40)
    time.sleep(2)

    # 验证代理和网页,验证通过EXECUTE_READY=True,否则为False
    authentication_engine()

    # 如果验证执行通过，开始执行网页引擎
    if EXECUTE_READY:
        page_engine()
    else:
        print("<-> 验证未通过，重新运行")

    # 如果数据库引擎执行完毕，开始执行数据推送引擎
    if TOTAL_PUSH_READY:
        push_engine()
    else:
        print("<-> 网页无更新或下载错误，重新运行")

    # 如果数据推送引擎执行完毕，则自动关闭整个引擎
    if PUSH_DONE:
        print("<+> 全流程执行成功，重新运行")
    else:
        print("<-> 网页推送错误，重新运行")


######## 开始执行 ########
if __name__ == "__main__":
    # 一直循环执行主函数，判断招标时间有没有跟新获取招标信息
    while True:
        start = time.clock()
        main()
        end = time.clock()
        print("<+> 执行消耗时长：{0}".format(end-start))
        print('<*> 程序等待中........\n')
        time.sleep(600)


