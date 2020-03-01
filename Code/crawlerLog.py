#!D:\Anaconda3\python.exe
# -*- coding: utf-8 -*-
'''
# Author  : CJH
# Time    : 2019-12-11
# File    : crawlerLog.py
# Version : 1.0.0
# Describe: 爬虫日志
# Update  :
'''

import logging
import datetime

LOG_PATH = r'H:\DIBS\log\crawlerLog_{0}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d'))
filer = logging.FileHandler(LOG_PATH)
filer.setLevel(logging.DEBUG)
consoler = logging.StreamHandler()
consoler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
filer.setFormatter(formatter)
consoler.setFormatter(formatter)

class CrawlerLog(object):
    def __init__(self, log_location):
        self.logger = logging.getLogger(log_location)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(filer)
        self.logger.addHandler(consoler)

    def debug(self, message_debug):
        self.logger.debug(message_debug)

    def info(self, message_info):
        self.logger.info(message_info)

    def warning(self, message_warn):
        self.logger.warning(message_warn)

    def error(self, message_error):
        self.logger.error(message_error)

    def exception(self, message_exception):
        self.logger.exception(message_exception)

    def critical(self, message_critical):
        self.logger.critical(message_critical)













