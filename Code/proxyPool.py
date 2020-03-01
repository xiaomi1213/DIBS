#!D:\Anaconda3\python.exe
# -*- coding: utf-8 -*-
'''
# Author  : CJH
# Time    : 2019-12-13
# File    : proxyPool.py
# Version : 1.0.0
# Describe: 构建代理池
# Update  :
'''


import requests
import random
import re
import traceback
from scrapy.selector import Selector
import configManager
from dbOperation import MysqlOperate


# 初始化代理池，爬取和存储代理到数据库，以及从数据库中抽取数据
class ProxyPool(object):
    def __init__(self):
        print("<*> 正在初始化代理池.....")
        self.User_Agent = random.choice(configManager.User_Agent)
        self.proxy_url = configManager.url_proxy['proxyURL1']


    def crawlProxy(self):
        """
        爬取、解析、清洗代理IP，并存储到数据库中
        :return: 代理 IP()
        """
        try:
            print("<*> 开始爬取数据")
            headers = {"User-Agent":self.User_Agent}
            # res = requests.get(self.proxy_url+'/nn/1', headers=headers).text
            # p_nums = '<a href="/nn/.*?">(.*?)</a>'
            # page_nums = re.findall(p_nums, res, re.S)
            # page_num = int(page_nums[3])
            page_num = 3
            for page in range(page_num):
                proxy_list = []
                proxy_url_n = self.proxy_url + '/nn/' + str(page)
                html = requests.get(proxy_url_n, headers=headers, timeout=20).text
                selector = Selector(text=html)
                all_trs = selector.css("#ip_list tr")
                for tr in all_trs[1:]:
                    speed_str = tr.css(".bar::attr(title)").extract()[0]
                    if speed_str:
                        speed = float(speed_str.split("秒")[0])
                    else:
                        speed = "none"
                    all_texts = tr.css("td::text").extract()

                    ip = all_texts[0]
                    port = all_texts[1]
                    protocal = all_texts[5]
                    proxy_list.append((protocal, ip, port, speed))
                print("<+> 第%d页爬取成功" %page)

                print("<*> 开始存储第%d页代理" %page)
                DB = MysqlOperate().db
                cur = DB.cursor()
                for proxy in proxy_list:
                    order = 'insert into proxy values(%s,%s,%s,%s)'
                    cur.execute(order, (proxy[0],proxy[1],proxy[2],proxy[3]))
                    DB.commit()
                    print("<+> 存储成功:{0}://{1}:{2}-{3}".format(proxy[0],proxy[1],proxy[2],proxy[3]))
                print("<+> 第%d页存储成功" %page)
                cur.close()
                DB.close()

        except:
            print("<-> 爬取失败")
            traceback.print_exc()

    def getProxy(self):
        """
        从数据库中随机获取一个可以用的代理
        :return:返回字典类型的取值结果
        """
        try:
            print("<*> 正在从数据库中随机获取代理 IP")
            DB = MysqlOperate().db
            cur = DB.cursor()
            order = 'select * from proxy ORDER BY RAND() LIMIT 1'
            cur.execute(order)
            random_proxy = cur.fetchall()[0]
            DB.commit()
            cur.close()
            DB.close()
            print("<+> 随机IP为:  {0}:{1}:{2}".format(random_proxy[0],random_proxy[1], random_proxy[2]))
            print("<+> 获取代理成功")
            return random_proxy
        except:
            print("<-> 获取代理失败")
            traceback.print_exc()

    def rebuildProxy(self):
        """
        重建代理池
        :return:
        """
        print("<*> 开始清理代理池")
        try:
            # 清除表内容，不能用drop方法，这样会将整个表删除
            DB = MysqlOperate().db
            cur = DB.cursor()
            cur.execute('truncate proxy')
            DB.commit()
            cur.close()
            DB.close()
            print("<+> 清理完成")
            self.crawlProxy()
        except:
            print("<-> 清理失败")
            traceback.print_exc()




if __name__ == '__main__':
    proxy_pool = ProxyPool()
    #proxy_pool.crawlProxy()
    #proxy_pool.rebuildProxy()
    proxy_pool.getProxy()



