# coding = utf8

import os

os.path.abspath(".")

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "792607724@qq.com"  # 用户名
mail_pass = "kvujhbtkwjkgbcda"  # 口令

sender = "792607724@qq.com"
receivers = ["792607724@qq.com"]


def send_mail(message_content, subject_content):
    message = MIMEText(message_content, "plain", "utf-8")
    message["From"] = Header("Python自动化运行脚本", "utf-8")
    message["To"] = Header("脚本开发者-陈广涛", "utf-8")

    subject = subject_content
    message["Subject"] = Header(subject, "utf-8")

    try:
        smtpObject = smtplib.SMTP()
        smtpObject.connect(mail_host, 25)
        smtpObject.login(mail_user, mail_pass)
        smtpObject.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error,无法发送邮件！！!")


if __name__ == '__main__':
    send_mail(message_content="测试邮箱发送功能", subject_content="测试邮件主题")
