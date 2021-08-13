#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import time

#表单数据
post_addr="https://10.105.1.35/srun_portal_pc_en.php?url=&ac_id=12"
post_header={
    'Host': '10.105.1.35',
    'Connection': 'keep-alive',
    'Content-Length': '130',
    'Accept': '*/*',
    'Origin': 'https://10.105.1.35',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://10.105.1.35/srun_portal_pc_en.php?url=&ac_id=12',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cookie': "double_stack_login=bQ0pOyR6IX%252Fu0akbf5QES0glrNeCGpyO0W87in3s6NboH%252FY5ecIFP5u%252BnbvVX3jK%252FDmXgJq3pvwUX%252Fuu2FeMeC%252B5MRH%252B832Ecn5qdLnWpnLW7l8GXblowSplyBFSmjGtsq%252B%252F1P1FhgHYqfsPt3DnfqlAviyhz3nPySVva2eI3l4reSWcbAy%252BZFcNadIUuxMnOP9Z57IQVGKtsSM6V%252FOat60%253D; login=bQ0o5ZADI11BgO3HLndd%252Bxt3LbV4WDOukYku0w8lLzexBDN9apD9W1lbrPqoG1SiwYf5QuQIMM4FpyQv6XtHlbiJD6lTBwppRWKCLqEJJLLGHxt8MhlLkAsRIkTwrEYW3U%252FiNB2zYdjO%252BOabNpJOe%252FbLd5H9%252BHO6xFjooyDM8VNmYnnjaNRJn3V4%252FAsCf6EREykVpec%253D",
    }
post_data= {'action': 'login',
            'username': 'yaoding.17%40intl.zju.edu.cn',
            'password': "You'rewrong",
            'ac_id': '12',
            'user_ip': '',
            'nas_ip': '',
            'user_mac':'',
            'url': '',
            "save_me": "1",
            'ajax':'1',
            }
#获取ip地址
import os
ipzip = os.popen("ifconfig")
ip=""

for i in ipzip:
    ip+=str(i)

def ip():
    ipzip = os.popen("ifconfig")
    ip=""
    for i in ipzip:
        ip+=str(i)
    return ip

import datetime
#发送文本内容

def ipnote_message():
    ipaddr=ip()
    HASH512="hex: dff69078fae204910e63113e303f64803fee885feef611f8696df3ff01a39fb164e424f7f3b7de5a8875dfd8a99a16480687b5e07007b7481f40b62736cdd483"
    nowtime_email=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    name_of_hardward="YD's Macbook Pro"
    msg="ip地址：\n"+str(ipaddr)+"\n设备："+name_of_hardward+"\n当前时间："+str(nowtime_email)+"\nverified via\n"+HASH512
    return msg

#使用邮箱发送
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def email(msg):
    sender = "frankydc@qq.com"
    receivers = ["frankydc@qq.com"]
    # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 第三方 SMTP 服务
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="frankydc@qq.com"    #用户名
    mail_pass="rfzxiyvmxqxobfca"   #口令

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(msg, "plain", "utf-8")
    message["From"] = Header("ip_note", "utf-8")     # 发送者
    message["To"] =  Header("ip_note", "utf-8")          # 接收者
    subject = "获取硬件IP"
    message["Subject"] = Header(subject, "utf-8")
    smtpObj = smtplib.SMTP("smtp.qq.com",587)
    smtpObj.connect(mail_host, 587)    # 25 为 SMTP 端口号
    #TLS加密
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.ehlo()
    #加密结束，并登陆，Outlook需要二重认证申请授权码，不然会被当作垃圾邮件

    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.close()
    print("email sent to "+mail_user)

#发送表单的逻辑
def login():
    print("now the time is "+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    return1=os.system('ping 114.114.114.114  -c 5')
    if return1:                                             #检测网络是否连接
        print ('Connection failed. Trying to login to networks of Intl Campus')
        try:
            requests.post(post_addr,data=post_data,headers=post_header, verify=False)
            print("sent")
            email(ipnote_message())
        except:
            print("The email is undeliverable...")
            print("the time of tis trial is"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    else:
        print ("Checking connection regularly...")

while True:
    n=0
    try:
        login()
    except:
        time.sleep(10)
