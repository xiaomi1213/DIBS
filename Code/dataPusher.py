#!D:\Anaconda3\python.exe
# -*- coding: utf-8 -*-
'''
# Author  : CJH
# Time    : 2019-12-14
# File    : dataPusher.py
# Version : 1.0.0
# Describe: 生成邮件正文，发送邮件
# Update  : 待解决写邮件的输出问题
'''

from dbOperation import MysqlOperate
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import parseaddr, formataddr
from email import encoders
import pandas as pd
import traceback



class DataPusher(object):
    def __init__(self):
        print("<*> 正在实例化推送器.....")

    def writeMail(self):
        # 获取上次存储的时间
        # tender_info = dbOperation.MongoOperate().collection1
        # last_time = end
        # tender_time = tender_info.find({"datetimes": {"$gt": last_time}}, {"_id": 0, "datetimes":1})
        # datetimes_list = [datetime.strptime(i,"%Y-%m-%d %H:%M") for i in tender_time]
        # start = datetime.strftime(min(datetimes_list),"%Y-%m-%d %H:%M")
        # end = datetime.strftime(max(datetimes_list),"%Y-%m-%d %H:%M")
        # 获取更新时间内的信息，装换为DataFrame格式
        # tender = tender_info.find_one({},{"_id": 0})
        # tender_df = pd.DataFrame(tender,index=[0])
        #tenders = tender_info.find({"datetimes":{"$gte":start,"$lte":end}},{"_id":0})
        # tenders = tender_info.find({"send":"no"},{"_id":0})
        # for t in tenders:
        #     t_s = pd.Series(t)
        #     tender_df = tender_df.append(t_s, ignore_index=True)
        # tender_info.update({"send":"no"},{"$set":{"send":"yes"}})

        # 获取发送字段为no的记录
        DB = MysqlOperate().db
        cur = DB.cursor()
        order1 = 'select * from tenders where send=%s'
        cur.execute(order1,("no"))
        tender_list = list(cur.fetchall())
        # 获取更新时间内的信息，装换为DataFrame格式
        tender_df = pd.DataFrame(tender_list,
                                 columns=['source','datetimes','titles','budgets','deadlines','hrefs','send'])
        # 获取发送字段为yes
        order2 = 'update tenders set send=%s where send=%s'
        cur.execute(order2, ("yes","no"))
        DB.commit()
        cur.close()
        DB.close()

        end = max(tender_df['datetimes']).split(' ')[0]
        start = min(tender_df['datetimes']).split(' ')[0]

        # 生成邮件正文文字
        mail_text = """
        <p><b>以下内容为{0}至{1}的招投标信息，详情请看Excel附件。</b></p>
        """.format(start,end)
        # 生成邮件正文表格
        old_width = pd.get_option('display.max_colwidth')  # 先把原来的显示列宽存下来
        pd.set_option('display.max_colwidth', -1)  # 设置一个新的列宽，宽度是-1，应该是显示宽度去自适应内容
        mail_table = tender_df.to_html(
                                       escape=False, index=False, sparsify=True,
                                        border=2, index_names=False)  # escape是指，要不要把单元格的内容中那些像html的标签，就写成html的标签，否则，就是纯文本形式。
        pd.set_option('display.max_colwidth', old_width)  # 把df的显示列宽恢复到默认值

        # 生成Excel邮件附件
        print("<*> 正在生成招投标信息文件.....")
        #attachment_path = "H:\\DIBS\\tenders\\tenders_%s %s.xlsx"%(start,end)
        attachment_path = "H:\\DIBS\\tenders\\tenders_{0}~{1}.xlsx".format(start,end)
        try:
            tender_df.to_excel(attachment_path, index=False)
            print("<+> 生成招投标信息文件成功")
        except:
            print("<-> 生成招投标信息文件失败")
            traceback.print_exc()
        return mail_text, mail_table, attachment_path

    def formatAddr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def sendMail(self, mail_text, mail_table, attachment_path):
        """
        发送邮件
        :param :
        :param attachment: 附件地址
        :return: 发送成功返回 True，否则返回 False
        """
        print("<*> 开始发送邮件.....")
        # QQ邮箱服务器
        smtp_server = ('smtp.qq.com', 465)
        # QQ邮箱授权码
        mail_pwd = 'qecctnbkamuabiie'
        # 要发送的邮箱用户名
        from_mail = '421751563@qq.com'
        # 接收的邮箱
        to_mail = 'chenjunhang2013@163.com'

        # 构造一个 MIMEMultipart 对象代表邮件本身
        msg = MIMEMultipart()
        msg['From'] =self.formatAddr('招投标信息爬虫 <%s>' % from_mail)
        msg['To'] = self.formatAddr('领导 <%s>' % to_mail)
        msg['Subject'] = Header(attachment_path.split('\\')[-1].split('.')[0].split('_')[-1]+'_招投标信息','utf-8').encode()

        # 邮件正文文字, plain 代表纯文本
        #msg.attach(MIMEText(mail_text, 'plain', 'utf-8'))
        # 邮件正文表格
        msg.attach(MIMEText(mail_text+mail_table, 'html', 'utf-8'))
        # 邮件附件，二进制模式文件
        with open(attachment_path, 'rb') as excel:
            # 添加附件就是加上一个MIMEBase,# 设置附件的MIME和文件名，这里是xls类型
            mime = MIMEApplication(excel.read())
            mime['Content-Type'] = 'application/octet-stream'
            mime['Content-Disposition'] = 'attachment; filename="{0}"'.format(attachment_path.split('\\')[-1])
            # 加上必要的头信息
            # mime.add_header('Content-Disposition', 'attachment', filename=attachment_path.split('\\')[-1])
            # mime.add_header('Content-ID','<0>')
            # mime.add_header('X-Attachment-Id','0')
            # 把附件的内容读进来
            # mime.set_payload(excel.read())
            # 用Base64编码
            # encoders.encode_base64(mime)
            # 作为附件添加到邮件
            msg.attach(mime)

        print("<*> 正在连接 SMTP 服务器.....")
        email = smtplib.SMTP_SSL(smtp_server[0], smtp_server[1])
        print("<+> 连接成功")
        print("<*> 正在授权 SMTP 服务.....")
        login_code = email.login(from_mail, mail_pwd)
        if login_code[0] is 235:
            print("<+> 授权成功")
        else:
            print("<-> 授权失败")
            return False
        try:
            # as_string() 把MIMEText 对象变成 str
            print("<+> 正在发送邮件")
            email.sendmail(from_mail, to_mail, msg.as_string())
            email.quit()
            print("<+> 发送成功")
            return True
        except:
            print("<-> 发送失败")
            traceback.print_exc()
            return False



if __name__ == "__main__":
    pusher = DataPusher()
    mail_text, mail_table, attachment_path = pusher.writeMail()
    # print(mail_text, mail_table)
    pusher.sendMail(mail_text, mail_table, attachment_path)



























