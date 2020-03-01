import re
import traceback



class DataClean(object):
    def __init__(self):
        print("<*> 正在实例化数据清洗模块.....")

    def cleanGDSZFCGW(self, resolved_data):
        print("<*> 开始清洗数据.....")
        datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list = resolved_data[0], resolved_data[1], resolved_data[2], resolved_data[3], \
                                                                                resolved_data[4]
        try:

            for i in range(len(hrefs_list)):
                # 数据清洗
                deadlines_list[i] = re.sub("<.*?>", '', deadlines_list[i])
                deadlines_list[i] = re.sub("年", '-', deadlines_list[i])
                deadlines_list[i] = re.sub("月", '-', deadlines_list[i])
                deadlines_list[i] = re.sub("日", ' ', deadlines_list[i])
                deadlines_list[i] = re.sub("时", ':', deadlines_list[i])
                deadlines_list[i] = re.sub("分", '', deadlines_list[i])
                if len(deadlines_list[i]) > 22:
                    deadlines_list[i] = deadlines_list[i][0:22]

                budgets_list[i] = budgets_list[i].strip()

                hrefs_list[i] = 'http://www.gdgpo.gov.cn/showNotice/id/' + hrefs_list[i] + '.html'
            print("<+> 数据清洗成功")
            cleaned_data = [datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list]
            return cleaned_data
        except:
            print("<-> 数据清洗失败")
            traceback.print_exc()
            return [[],[],[],[],[]]

    def cleanGZGGZYJYGGFWPT(self, resolved_data):
        print("<*> 开始清洗数据.....")
        datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list = resolved_data[0], resolved_data[1], resolved_data[2], resolved_data[3], \
                                                                                resolved_data[4]
        try:

            for i in range(len(hrefs_list)):
                # 数据清洗
                deadlines_list[i] = re.sub("年", '-', deadlines_list[i])
                deadlines_list[i] = re.sub("月", '-', deadlines_list[i])
                deadlines_list[i] = re.sub("日", ' ', deadlines_list[i])
                datetimes_list[i] = datetimes_list[i].strip()

            print("<+> 数据清洗成功")
            cleaned_data = [datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list]
            return cleaned_data
        except:
            print("<-> 数据清洗失败")
            traceback.print_exc()
            return [[],[],[],[],[]]

    def cleanSZSGGZYJYPT(self, resolved_data):
        pass


if __name__ == '__main__':
    from selenium import webdriver
    import time
    import configManager
    from pageResolver import PageResolver
    executable_path = r'D:\Anaconda3\Scripts\chromedriver.exe'
    # executable_path = r'E:\ProgramData\Anaconda3\Scripts\chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)

    # 广东省政府采购网
    # url = configManager.tender_urls["广东省政府采购网"]
    # browser.get(url)
    # time.sleep(2)
    # browser.maximize_window()
    # PageResolver().resovleGDSZFCGW(browser)

    # 广州公共资源交易公共服务平台
    url = configManager.tender_urls["广州公共资源交易公共服务平台"]
    browser.get(url)
    time.sleep(2)
    browser.maximize_window()
    resolved_data, update_flag = PageResolver().resovleGZGGZYJYGGFWPT(browser)
    cleaned_data = DataClean().cleanGZGGZYJYGGFWPT(resolved_data)
    print(cleaned_data)
