#!D:\Anaconda3\python.exe
# -*- coding: utf-8 -*-
'''
# Author  : CJH
# Time    : 2019-12-18
# File    : pageResolver.py
# Version : 1.0.0
# Describe: 解析网页中的时间、连接、标题、预算、截止时间等信息，
#           并检查网页信息是否更新，同时检查网页内容和资质
# Update  :
'''

import re
import time
import requests
import traceback
import random
import datetime
from selenium import webdriver
import configManager
from dbOperation import MysqlOperate

class PageResolver(object):
    def __init__(self):
        print('<*> 正在实例化网页解析器.....')

        self.executable_path=r'D:\Anaconda3\Scripts\chromedriver.exe'
        # self.executable_path = r'E:\ProgramData\Anaconda3\Scripts\chromedriver.exe'

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        # proxy = ProxyPool().getProxy()
        # chrome_options.add_argument("--proxy-server={0}://{1}:{2}".format
        #                             (proxy[0], proxy[1], proxy[2]))


        self.DB = MysqlOperate().db
        self.keywords = configManager.keywords
        self.qualifications = configManager.qualifications

    def resovleGDSZFCGW(self):
        try:
            print('<*> 正在解析网页.....')
            datetimes_list = []
            hrefs_list = []
            titles_list = []
            budgets_list = []
            deadlines_list = []
            # 获取数据库中上次的时间
            # last_time = self.table.find({}, {"datetimes": 1, "_id": 0}).sort("datetimes", -1).limit(1)
            # datetime_list = list(last_time)
            # last_time = datetime_list[0]["datetimes"]
            # last_time = datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M")
            order = 'select max(datetimes) from tenders where source=%s'
            cur = self.DB.cursor()
            cur.execute(order,'广东省政府采购网')
            last_time = cur.fetchall()[0][0]
            last_time = datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M")
            self.DB.commit()
            cur.close()
            self.DB.close()

            # 获取html网页信息
            browser = webdriver.Chrome(executable_path=self.executable_path, chrome_options=self.chrome_options)
            url = configManager.tender_urls["广东省政府采购网"]
            browser.get(url)
            time.sleep(2)
            browser.maximize_window()

            main_html = browser.page_source
            time.sleep(2)
            p_num = '<span class="aspan">(.*?)</span>'
            num = re.findall(p_num, main_html, re.S)
            page_num = int(num[-1]) - 1  # 减1防止索引溢出
            for i in range(page_num):
                print("<*> 正在解析第{0}个网页.....".format(i+1))
                # 解析时间，招标信息链接，标题，检查信息是否更新
                page_html = browser.page_source
                time.sleep(2)
                p_list = '<ul class="m_m_c_list">(.*?)</ul>'
                li_list = re.findall(p_list, page_html, re.S)
                lis = ''.join(li_list)
                p_datetime = '<em>(.*?)</em>'
                p_href = '<a href="/showNotice/id/(.*?).html"'
                p_title = '<a href=".*?title="(.*?)">'
                datetimes = re.findall(p_datetime, lis, re.S)
                hrefs = re.findall(p_href, lis, re.S)
                titles = re.findall(p_title, lis, re.S)
                # 检查网页招标信息是否更新
                # 获取网页中最早和最晚时间
                html_time = [datetime.datetime.strptime(i,"%Y-%m-%d %H:%M") for i in datetimes]
                #min_time = min(html_time)
                max_time = max(html_time)
                # 若数据库中上次的时间大于本次网页最大时间，则退出本次爬取
                if last_time >= max_time:
                    print('<-> 此网页招标信息未更新，本次爬取结束，处理已爬取网页')
                    break
                else:
                    for i in range(len(html_time)):
                        if html_time[i] > last_time:
                            datetimes[i] = datetimes[i]
                            hrefs[i] = hrefs[i]
                            titles[i] = titles[i]
                        else:
                            datetimes[i] = "none"
                            hrefs[i] = "none"
                            titles[i] = "none"
                    deadlines = []
                    budgets = []
                    for j in range(len(hrefs)):
                        time.sleep(1)
                        if hrefs[j] != "none":
                            full_href = 'http://www.gdgpo.gov.cn/showNotice/id/' + hrefs[j] + '.html'
                            User_Agent = random.choice(configManager.User_Agent)
                            headers = {"User-Agent": User_Agent}
                            content_html = requests.get(full_href, headers=headers).text
                            p_budget = '<div class="zw_c_c_qx">.*?<span>预算金额：(.*?)元</span>.*?</div>'
                            p_deadline = '<p style="text-indent:.*?截止时间：(.*?)</span></p>'
                            budget = re.findall(p_budget, content_html, re.S)
                            deadline = re.findall(p_deadline, content_html, re.S)

                            # 检查网页招标信息是否适合
                            keyword_count = 0
                            for keyword in self.keywords:
                                if keyword in content_html:
                                    keyword_count += 1
                            if keyword_count < 1:
                                print("<-> 此招标信息不符合公司业务，此次爬取终止，继续爬取下一页信息")
                                datetimes[j] = "none"
                                hrefs[j] = "none"
                                titles[j] = "none"
                                budgets.append("none")
                                deadlines.append("none")
                            else:
                                if len(deadline) != 0:
                                    deadlines.append(deadline[0])
                                else:
                                    deadlines.append("null")
                                if len(budget) != 0:
                                    budgets.append(budget[0])
                                else:
                                    budgets.append("null")

                            # 检查网页招标信息是否符合资质
                            # qua_count = 0
                            # for qua in self.qualifications:
                            #     if qua in content_html:
                            #         qua_count += 1
                            # if qua_count < 1:
                            #     print("<-> 公司资质不符合此招标信息，此次爬取终止，继续爬取下一条信息")
                            #     datetimes[i] = "none"
                            #     hrefs[i] = "none"
                            #     titles[i] = "none"
                            #     budgets[i] = "none"
                            #     deadlines[i] = "none"
                            #     break

                datetimes_list.extend(datetimes)
                hrefs_list.extend(hrefs)
                titles_list.extend(titles)
                budgets_list.extend(budgets)
                deadlines_list.extend(deadlines)

                browser.find_element_by_xpath('//*[@id="contianer"]/div[3]/div[2]/div[3]/div/form/a[8]/span').click()

            browser.quit()

            # 清除“none”值
            while "none" in datetimes_list:
                datetimes_list.remove("none")
            while "none" in hrefs_list:
                hrefs_list.remove("none")
            while "none" in titles_list:
                titles_list.remove("none")
            while "none" in budgets_list:
                budgets_list.remove("none")
            while "none" in deadlines_list:
                deadlines_list.remove("none")

            if len(deadlines_list) < 1:
                print("<-> 网页解析成功，但并无信息更新")
                update_flag = False
                resolved_data = [[],[],[],[],[]]
                return resolved_data, update_flag
            else:
                print("<+> 网页解析成功，已有信息更新")
                update_flag = True
                resolved_data = [datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list]
                #print(len(datetimes_list),len(hrefs_list),len(titles_list),len(budgets_list),len(deadlines_list))
                print('<+> 解析的信息条数：%d'%len(deadlines_list))
                return resolved_data, update_flag



        except:
            print('<-> 网页解析失败')
            traceback.print_exc()
            return [[],[],[],[],[]],False

    def resovleGZGGZYJYGGFWPT(self):
        try:
            print('<*> 正在解析网页.....')
            datetimes_list = []
            hrefs_list = []
            titles_list = []
            budgets_list = []
            deadlines_list = []

            # 获取数据库中上次的时间
            order = 'select max(datetimes) from tenders where source=%s'
            cur = self.DB.cursor()
            cur.execute(order,'广州公共资源交易公共服务平台')
            last_time = cur.fetchall()[0][0]
            try:
                last_time = datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M")
            except:
                last_time = datetime.datetime.strptime(last_time, "%Y-%m-%d")
            self.DB.commit()
            cur.close()
            self.DB.close()

            # 获取html网页信息
            browser = webdriver.Chrome(executable_path=self.executable_path, chrome_options=self.chrome_options)
            url = configManager.tender_urls["广州公共资源交易公共服务平台"]
            browser.get(url)
            time.sleep(2)
            browser.maximize_window()

            main_html = browser.page_source
            time.sleep(1)
            p_num = '<div class="green-black">.*?/共(.*?)页.*?</div>'
            num = re.findall(p_num, main_html, re.S)
            page_num = int(num[0]) - 1  # 减1防止索引溢出
            for i in range(page_num):
                print("<*> 正在解析第{0}个网页.....".format(i+1))
                # 解析时间，招标信息链接，标题，检查信息是否更新
                page_html = browser.page_source
                time.sleep(1)
                p_list = '<div class="prcont TableListLine".*?<ul>(.*?)<div class="pagesite">'
                li_list = re.findall(p_list, page_html, re.S)
                lis = ''.join(li_list)
                p_datetime = '<span class="floR colorCCC">(.*?)</span>'
                p_href = '<a href="(.*?)" target="_blank"'
                p_title = '<a href=".*?title="(.*?)">'
                datetimes = re.findall(p_datetime, lis, re.S)
                hrefs = re.findall(p_href, lis, re.S)
                titles = re.findall(p_title, lis, re.S)

                # 检查网页招标信息是否更新
                # 获取网页中最早和最晚时间
                html_time = [datetime.datetime.strptime(i.strip(),"%Y-%m-%d") for i in datetimes]
                #min_time = min(html_time)
                max_time = max(html_time)
                # 若数据库中上次的时间大于本次网页最大时间，则退出本次爬取
                if last_time >= max_time:
                    print('<-> 此网页招标信息未更新，本次爬取结束，处理已爬取网页')
                    break
                else:
                    for i in range(len(html_time)):
                        if html_time[i] > last_time:
                            datetimes[i] = datetimes[i]
                            hrefs[i] = hrefs[i]
                            titles[i] = titles[i]
                        else:
                            datetimes[i] = "none"
                            hrefs[i] = "none"
                            titles[i] = "none"
                    deadlines = []
                    budgets = []
                    for j in range(len(hrefs)):
                        time.sleep(1)
                        if hrefs[j] != "none":
                            User_Agent = random.choice(configManager.User_Agent)
                            headers = {"User-Agent": User_Agent}
                            content_html = requests.get(hrefs[j], headers=headers).text
                            p_budget = '预算金额.*?人民币(.*?)元'
                            p_deadline = '<a name="EB053b400bade94be288048635d81830c9">.*?">(.*?)</span>'
                            budget = re.findall(p_budget, content_html, re.S)
                            deadline = re.findall(p_deadline, content_html, re.S)
                            # 检查网页招标信息是否适合
                            keyword_count = 0
                            for keyword in self.keywords:
                                if keyword in content_html:
                                    keyword_count += 1
                            if keyword_count < 1:
                                print("<-> 此招标信息不符合公司业务，此次爬取终止，继续爬取下一页信息")
                                datetimes[j] = "none"
                                hrefs[j] = "none"
                                titles[j] = "none"
                                budgets.append("none")
                                deadlines.append("none")
                            else:
                                if len(deadline) != 0:
                                    deadlines.append(deadline[0])
                                else:
                                    deadlines.append("null")
                                if len(budget) != 0:
                                    budgets.append(budget[0])
                                else:
                                    budgets.append("null")

                datetimes_list.extend(datetimes)
                hrefs_list.extend(hrefs)
                titles_list.extend(titles)
                budgets_list.extend(budgets)
                deadlines_list.extend(deadlines)

                browser.find_element_by_xpath('/html/body/div[6]/div[2]/ul/div/div/div/a[10]').click()
            # 清除“none”值
            while "none" in datetimes_list:
                datetimes_list.remove("none")
            while "none" in hrefs_list:
                hrefs_list.remove("none")
            while "none" in titles_list:
                titles_list.remove("none")
            while "none" in budgets_list:
                budgets_list.remove("none")
            while "none" in deadlines_list:
                deadlines_list.remove("none")

            if len(deadlines_list) < 1:
                print("<-> 网页解析成功，但并无信息更新")
                update_flag = False
                resolved_data = [[], [], [], [], []]
                return resolved_data, update_flag
            else:
                print("<+> 网页解析成功，已有信息更新")
                update_flag = True
                resolved_data = [datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list]
                print('<+> 解析的信息条数：%d' % len(deadlines_list))
                return resolved_data, update_flag
        except:
            print('<-> 网页解析失败')
            traceback.print_exc()
            return [[], [], [], [], []], False

    def resovleSZSGGZYJYPT(self):
        try:
            print('<*> 正在解析网页.....')
            datetimes_list = []
            hrefs_list = []
            titles_list = []
            budgets_list = []
            deadlines_list = []
            # 获取数据库中上次的时间
            order = 'select max(datetimes) from tenders where source=%s'
            cur = self.DB.cursor()
            cur.execute(order,'深圳市公共资源交易平台')
            last_time = cur.fetchall()[0][0]
            last_time = datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M")
            self.DB.commit()
            cur.close()
            self.DB.close()

            # 获取html网页信息
            browser = webdriver.Chrome(executable_path=self.executable_path, chrome_options=self.chrome_options)
            url = configManager.tender_urls["深圳市公共资源交易平台"]
            browser.get(url)
            time.sleep(2)
            browser.maximize_window()

            main_html = browser.page_source
            time.sleep(3)
            p_num = '<div class="page">.*?总共(.*?)页</font>'
            num = re.findall(p_num, main_html, re.S)
            page_num = int(num[0]) - 1  # 减1防止索引溢出
            for i in range(page_num):
                print("<*> 正在解析第{0}个网页.....".format(i+1))
                # 解析时间，招标信息链接，标题，检查信息是否更新
                page_html = browser.page_source
                time.sleep(2)
                p_list = '<div class="tag-list4">(.*?)</div>'
                li_list = re.findall(p_list, page_html, re.S)
                lis = ''.join(li_list)
                p_datetime = '<span>(.*?)</span>'
                p_href = '<a href=".(.*?)"'
                p_title = '<a href=".*?title="(.*?)">'
                datetimes = re.findall(p_datetime, lis, re.S)
                hrefs = re.findall(p_href, lis, re.S)
                titles = re.findall(p_title, lis, re.S)
                # 检查网页招标信息是否更新
                # 获取网页中最早和最晚时间
                html_time = [datetime.datetime.strptime(i,"%Y-%m-%d") for i in datetimes]
                #min_time = min(html_time)
                max_time = max(html_time)
                # 若数据库中上次的时间大于本次网页最大时间，则退出本次爬取
                if last_time >= max_time:
                    print('<-> 此网页招标信息未更新，本次爬取结束，处理已爬取网页')
                    break
                else:
                    for j in range(len(html_time)):
                        if html_time[j] > last_time:
                            datetimes[j] = datetimes[j]
                            hrefs[j] = hrefs[j]
                            titles[j] = titles[j]
                        else:
                            datetimes[j] = "none"
                            hrefs[j] = "none"
                            titles[j] = "none"
                    # print(datetimes,hrefs,titles)
                    deadlines = []
                    budgets = []
                    for j in range(len(hrefs)):
                        time.sleep(1)
                        if hrefs[j] != "none":
                            full_href = 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/sbj/zbgg' + hrefs[j]
                            User_Agent = random.choice(configManager.User_Agent)
                            headers = {"User-Agent": User_Agent}
                            content_html = requests.get(full_href, headers=headers).text.encode('ISO-8859-1').decode('utf-8')

                            p_budget = '<td>.*?<p align="center">(.*?)</p>.*?</td>'
                            budgetlist = re.findall(p_budget, content_html, re.S)
                            budget = budgetlist[budgetlist.index(re.compile('预算*.?'))+1]
                            if budget < 10000:
                                budget = re.findall(p_budget, content_html, re.S)[-1]

                            p_deadline = '报价截止时间：</span><span id="holder">(.*?)</span>'
                            deadline = re.findall(p_deadline, content_html, re.S)
                            if len(deadline) < 1:
                                p_deadline = ''
                                deadline = re.findall(p_deadline, content_html, re.S)

                            print(budget,deadline)
            #
            #                 # 检查网页招标信息是否适合
            #                 keyword_count = 0
            #                 for keyword in self.keywords:
            #                     if keyword in content_html:
            #                         keyword_count += 1
            #                 if keyword_count < 1:
            #                     print("<-> 此招标信息不符合公司业务，此次爬取终止，继续爬取下一页信息")
            #                     datetimes[j] = "none"
            #                     hrefs[j] = "none"
            #                     titles[j] = "none"
            #                     budgets.append("none")
            #                     deadlines.append("none")
            #
            #                 else:
            #                     if len(deadline) != 0:
            #                         deadlines.append(deadline[0])
            #                     else:
            #                         deadlines.append("null")
            #                     if len(budget) != 0:
            #                         budgets.append(budget[0])
            #                     else:
            #                         budgets.append("null")
            #
            #                 # 检查网页招标信息是否符合资质
            #                 # qua_count = 0
            #                 # for qua in self.qualifications:
            #                 #     if qua in content_html:
            #                 #         qua_count += 1
            #                 # if qua_count < 1:
            #                 #     print("<-> 公司资质不符合此招标信息，此次爬取终止，继续爬取下一条信息")
            #                 #     datetimes[i] = "none"
            #                 #     hrefs[i] = "none"
            #                 #     titles[i] = "none"
            #                 #     budgets[i] = "none"
            #                 #     deadlines[i] = "none"
            #                 #     break
            #
            #     datetimes_list.extend(datetimes)
            #     hrefs_list.extend(hrefs)
            #     titles_list.extend(titles)
            #     budgets_list.extend(budgets)
            #     deadlines_list.extend(deadlines)
            #
                if i == 0:
                    browser.find_element_by_xpath('//*[@id="tagContent"]/div/div/div[4]/a[1]').click()
                    print('heheheh')
                browser.find_element_by_xpath('//*[@id="tagContent"]/div/div/div[4]/a[3]').click()

            #
            # #print(len(datetimes_list), len(hrefs_list), len(titles_list), len(budgets_list), len(deadlines_list))
            # # 清除“none”值
            # while "none" in datetimes_list:
            #     datetimes_list.remove("none")
            # while "none" in hrefs_list:
            #     hrefs_list.remove("none")
            # while "none" in titles_list:
            #     titles_list.remove("none")
            # while "none" in budgets_list:
            #     budgets_list.remove("none")
            # while "none" in deadlines_list:
            #     deadlines_list.remove("none")
            #
            # if len(deadlines_list) < 1:
            #     print("<-> 网页解析成功，但并无信息更新")
            #     update_flag = False
            #     resolved_data = [[],[],[],[],[]]
            #     return resolved_data, update_flag
            # else:
            #     print("<+> 网页解析成功，已有信息更新")
            #     update_flag = True
            #     resolved_data = [datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list]
            #     #print(len(datetimes_list),len(hrefs_list),len(titles_list),len(budgets_list),len(deadlines_list))
            #     print('<+> 解析的信息条数：%d'%len(deadlines_list))
            #     return resolved_data, update_flag

        except:
            print('<-> 网页解析失败')
            traceback.print_exc()
            return [[],[],[],[],[]],False


if __name__ == "__main__":

    # 广东省政府采购网
    PageResolver().resovleGDSZFCGW()

    # 广州公共资源交易公共服务平台
    resolved_data, update_flag = PageResolver().resovleGZGGZYJYGGFWPT()
    print(resolved_data, update_flag)

    # 深圳市公共资源交易平台
    # PageResolver().resovleSZSGGZYJYPT()

