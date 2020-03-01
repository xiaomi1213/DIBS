from dbOperation import MysqlOperate
import traceback


class DataStore(object):
    def __init__(self):
        print("<*> 正在实例化数据库.....")


    def storeGDSZFCGW(self, data):
        try:
            datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list = data[0], data[1], data[2], data[3], \
                                                                                    data[4]

            print("<*> 开始存储数据.....")
            DB = MysqlOperate().db
            cur = DB.cursor()
            for i in range(len(hrefs_list)):
                order = 'insert into tenders values(%s,%s,%s,%s,%s,%s,%s)'
                cur.execute(order, (
                '广东省政府采购网',datetimes_list[i], titles_list[i], budgets_list[i], deadlines_list[i], hrefs_list[i],"no"))
            DB.commit()
            cur.close()
            DB.close()
                # data_dict = {"datetimes":datetimes_list[i], "href":hrefs_list[i], "titles":titles_list[i],
                #              "budgets":budgets_list[i], "deadlines":deadlines_list[i], "send":"no"}
                # self.DB.insert(data_dict)

            print("<+> 数据存储成功")
        except:
            print("<-> 数据存储失败")
            traceback.print_exc()

    def storeGZGGZYJYGGFWPT(self, data):
        try:
            datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list = data[0], data[1], data[2], data[3], \
                                                                                    data[4]

            print("<*> 开始存储数据.....")
            DB = MysqlOperate().db
            cur = DB.cursor()
            for i in range(len(hrefs_list)):
                order = 'insert into tenders values(%s,%s,%s,%s,%s,%s,%s)'
                cur.execute(order, (
                '广州公共资源交易公共服务平台',datetimes_list[i], titles_list[i], budgets_list[i], deadlines_list[i], hrefs_list[i],"no"))
            DB.commit()
            cur.close()
            DB.close()
            print("<+> 数据存储成功")
        except:
            print("<-> 数据存储失败")
            traceback.print_exc()

    def storeSZSGGZYJYPT(self, data):
        try:
            datetimes_list, hrefs_list, titles_list, budgets_list, deadlines_list = data[0], data[1], data[2], data[3], \
                                                                                    data[4]

            print("<*> 开始存储数据.....")
            DB = MysqlOperate().db
            cur = DB.cursor()
            for i in range(len(hrefs_list)):
                order = 'insert into tenders values(%s,%s,%s,%s,%s,%s,%s)'
                cur.execute(order, (
                '深圳市公共资源交易平台',datetimes_list[i], titles_list[i], budgets_list[i], deadlines_list[i], hrefs_list[i],"no"))
            DB.commit()
            cur.close()
            DB.close()
            print("<+> 数据存储成功")
        except:
            print("<-> 数据存储失败")
            traceback.print_exc()