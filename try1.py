import configManager
# import proxyPool
import random
from selenium import webdriver
import time
import re
import requests
#from dbOperation import MongoOperate


#executable_path=r'D:\Anaconda3\Scripts\chromedriver.exe'
executable_path=r'E:\ProgramData\Anaconda3\Scripts\chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# proxy = proxyPool.getProxy()
# protocol = proxy["protocol"]
# ip = proxy["ip"]
# port = proxy["port"]
# chrome_options.add_argument("--proxy-server={0}://{1}:{2}".format(protocol, ip, port))
browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)


# 获取html网页信息
url = configManager.tender_urls["广东省政府采购网"]
browser.get(url)
time.sleep(2)
browser.maximize_window()



# keywords = []
qualifications = []
datetimes_list = []
hrefs_list = []
titles_list = []
tendernos_list = []
deadlines_list = []
main_html = browser.page_source
p_num = '<span class="aspan">(.*?)</span>'
num = re.findall(p_num, main_html, re.S)
print(num)
page_num = int(num[-1])-1 # 减1防止索引溢出
print(page_num)
for i in range(2):
    # 网页解析
    page_html = browser.page_source
    time.sleep(1)
    p_list = '<ul class="m_m_c_list">(.*?)</ul>'
    li_list = re.findall(p_list, page_html, re.S)
    lis = ''.join(li_list)
    p_datetime = '<em>(.*?)</em>'
    p_href = '<a href="/showNotice/id/(.*?).html"'
    p_title = '<a href=".*?title="(.*?)">'

    datetimes = re.findall(p_datetime, lis, re.S)
    hrefs = re.findall(p_href, lis, re.S)
    titles = re.findall(p_title, lis, re.S)



# hrefs = ['40288ba96efa1cc7016efe0a254b085d', '40288ba96efa1cc7016efda1ecdc6897', '40288ba96efa1cc7016efd0ba8793823', '40288ba96efa1cc7016efd0efb483a07', '40288ba96ec2c35e016ef9da75a53396', '40288ba96ec2c35e016ef9ab575a2df0', '40288ba96ec2c35e016ef99f334a2b06', '40288ba96ec2c35e016ef9881b5e249b', '40288ba96ec2c35e016ef978dd0b1d27', '40288ba96ec2c35e016ef98b277d2648', '40288ba96ec2c35e016eef0841e2407b', '40288ba96ec2c35e016ef94f3ef5051b', '40288ba96ec2c35e016ef9641d2c1042', '40288ba96ec2c35e016ef9593300091e', '40288ba96ec2c35e016ef958ee5308c6']
    deadlines = []
    budgets = []
    for i in range(len(hrefs)):
        time.sleep(1)
        full_href = 'http://www.gdgpo.gov.cn/showNotice/id/' + hrefs[i] + '.html'
        User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        headers = {"User-Agent": User_Agent}
        content_html = requests.get(full_href,headers=headers).text
        p_budget = '<div class="zw_c_c_qx">.*?<span>预算金额：(.*?)元</span>.*?</div>'
        p_deadline = '<p style="text-indent:.*?截止时间：(.*?)</span></p>'
        budget = re.findall(p_budget, content_html, re.S)
        deadline = re.findall(p_deadline, content_html, re.S)
        print(budget)
        print(deadline)
        if len(deadline) != 0:
            deadlines.append(deadline[0])
        else:
            deadlines.append("none")
        if len(budget) != 0:
            budgets.append(budget[0])
        else:
            budgets.append("none")

    print('解析完成')

    # 数据清洗
    for i in range(len(hrefs)):
        deadlines[i] = re.sub("<.*?>",'',deadlines[i])
        deadlines[i] = re.sub("年", '-', deadlines[i])
        deadlines[i] = re.sub("月", '-', deadlines[i])
        deadlines[i] = re.sub("日", '', deadlines[i])
        deadlines[i] = re.sub("时", ':', deadlines[i])
        deadlines[i] = re.sub("分", '', deadlines[i])

        budgets[i] = budgets[i].strip()

    print('清洗完成')
    print(datetimes)
    print(hrefs)
    print(titles)
    print(deadlines)
    print(budgets)

# 剔除空元素
# while 'none' in datetimes:
#     datetimes.remove('none')
# while 'none' in hrefs:
#     hrefs.remove('none')
# while 'none' in titles:
#     titles.remove('none')
# while 'none' in tendernos:
#     tendernos.remove('none')
# datetimes_list.extend(datetimes)
# hrefs_list.extend(hrefs)
# titles_list.extend(titles)
# tendernos_list.extend(tendernos)
# deadlines_list.extend(deadlines)





