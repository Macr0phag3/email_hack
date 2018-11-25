# -*- coding: utf-8 -*-

import socket
import dns.resolver


class Email:
    '''
    just for FakeEmail and EmailBomb
    '''

    def __init__(self, to_addr, from_addr, SMTP_addrs, port, timeout):
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.port = port
        self.timeout = timeout
        self.SMTP_addrs = SMTP_addrs

    def DNSQuery(self):
        resolver = dns.resolver.Resolver()
        resolver.timeout = 3
        resolver.lifetime = 3

        try:
            host = self.to_addr[self.to_addr.find(u"@")+1:]

            # dns 列表
            self.SMTP_addrs = [b'.'.join(d.exchange.labels).decode(u"utf8") for d in dns.resolver.query(host, u'MX')]
            assert len(self.SMTP_addrs) > 1  # 确保 dns 有结果

        except Exception as e:
            return (False, u"get MX record of %s failed: " % self.to_addr + str(e))

        return (True, u"get MX record of %s success" % host)

    def Connect(self):
        # 获得 smtp 地址
        if not self.SMTP_addrs:  # 没有指定 smtp 的地址
            code, msg = self.DNSQuery()
            if not code:
                return (code, msg)

        for self.SMTP_addr in self.SMTP_addrs:
            try:
                self.sk = socket.socket()  # 失败后必须重新建立 socket
                self.sk.settimeout(self.timeout)  # 否则会出现 [Errno 37] Operation already in progress
                self.sk.connect((self.SMTP_addr, self.port))
                code, msg = self.Recv(check="220")  # 服务器返回 200 状态码才算成功
                if code:  # 成功则直接返回
                    break
                else:
                    err = msg
            except Exception as e:
                err = str(e)
        else:  # 没有 break，说明没有成功
            return (False, "connect to SMTP: "+self.SMTP_addr+":"+str(self.port)+" failed: "+err)

        return (True, "send connection request success")

    def Send(self, msgs, recv=True, check=""):
        '''
        msgs: 待发送的消息
        recv: 是否等待返回的消息
        '''

        for msg in msgs.split(u"\r\n"):
            try:
                self.sk.sendall((msg+u"\r\n").encode("utf8"))
            except Exception as e:
                err = str(e)
                break
        else:  # 发送成功
            if recv:  # 有返回的消息
                return self.Recv(check)
            else:
                return (True, "send(without reply) success")

        return (False, "send msg failed: "+err)

    def Recv(self, check=u""):
        try:
            data = [i.decode(u"utf8") for i in self.sk.recv(1024).split(b"\r\n") if i]
            assert data

        except AssertionError:
            return (False, u"recv empty answer")

        except Exception as e:
            return (False, "recv msg failed: "+str(e))

        if check and check not in data[-1]:  # 只检查最后一条消息
            return (False, "recv msg success but check failed: "+data[-1])

        # 400 - 600 为 smtp 的各种异常状态码
        if any([i for i in range(400, 600) if data[-1][:3] == str(i)]):
            return (False, "recv msg success but found error code: "+data[-1])

        return (True, data)
