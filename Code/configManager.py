#!D:\Anaconda3\python.exe
# -*- coding: utf-8 -*-
'''
# Author  : CJH
# Time    : 2019-12-13
# File    : configManager.py
# Version : 1.0.0
# Describe: 配置管理器，存储爬虫各模块配置参数
# Update  :
'''

# 浏览器头部名称
User_Agent = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",  # IE
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",  # Chrome
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",  # Firefox
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintoshl Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",  # Opera
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
    ]


url_proxy = {
    "proxyURL1": "http://www.xicidaili.com/",  # 代理 IP 网站
}

attachment_path = r"H:\DIBS\tenders"

# Mongodb 配置参数
MongodbParams = {
    "userName":"localhost",
    "port":27017,
    "collection1":"tender_info",
    "collection2":"log",
    "collection3":"proxy"
}

# MySQL 配置参数
MySQLParams = {
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"forjun598",
    "database":"Tender_DB",
    "charset":"utf8"
}


# 招标网站
tender_urls = {"广东省政府采购网":"http://www.gdgpo.gov.cn/queryMoreInfoList/channelCode/00051.html",
               "广州公共资源交易公共服务平台":"http://www.gzebpubservice.cn/cggg/index.htm",
                "深圳市公共资源交易平台":"http://ggzy.sz.gov.cn/cn/jyxx/zfcg/sbj/zbgg/index.htm"
               }

# 关键词
keywords = ['防伪','溯源','电子','智能','智慧',
            '大数据','云计算','区块链',
            '无线','wifi','WIFI','软件']

# 资质
qualifications = ['出入境检验检疫报检企业备案表','对外贸易经营者备案登记表','信息系统集成及服务资质（叁级）',
                  '进口肉类产品收货人备案','企业知识产权管理体系认证','GB/T 29490-2013','安防系统设计、施工、维修资格证']

# HTTP 状态码字典
httpStatusCode = {
    "300": "Multiple Choices",
    "301": "Moved Permanently",
    "302": "Move temporarily",
    "303": "See Other",
    "304": "Not Modified",
    "305": "Use Proxy",
    "306": "Switch Proxy",
    "307": "Temporary Redirect",
    "400": "Bad Request",
    "401": "Unauthorized",
    "402": "Payment Required",
    "403": "Forbidden",
    "404": "Not Found",
    "405": "Method Not Allowed",
    "406": "Not Acceptable",
    "407": "Proxy Authentication Required",
    "408": "Request Timeout",
    "409": "Conflict",
    "410": "Gone",
    "411": "Length Required",
    "412": "Precondition Failed",
    "413": "Request Entity Too Large",
    "414": "Request-URI Too Long",
    "415": "Unsupported Media Type",
    "416": "Requested Range Not Satisfiable",
    "417": "Expectation Failed",
    "421": "Too many connections",
    "422": "Unprocessable Entity",
    "423": "Locked",
    "424": "Failed Dependency",
    "425": "Unordered Collection",
    "426": "Upgrade Required",
    "449": "Retry With",
    "451": "Unavailable For Legal Reasons",
    "500": "Internal Server Error",
    "501": "Not Implemented",
    "502": "Bad Gateway",
    "503": "Service Unavailable",
    "504": "Gateway Timeout",
    "505": "HTTP Version Not Supported",
    "506": "Variant Also Negotiates",
    "507": "Insufficient Storage",
    "509": "Bandwidth Limit Exceeded",
    "510": "Not Extended",
    "600": "Unparseable Response Headers"
}