# -*- coding: utf-8 -*-
import dns.resolver
import socket


class EmailAgent:  # 邮件类
    def __init__(self, to_addr, from_addr, SMTP_addr, port=25, timeout=10):
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.port = port
        self.timeout = timeout
        self.SMTP_addr = SMTP_addr
        self.quit_flag = 1
        self.succ_num = 0
        self.failed_num = 0

    def Send(self):
        """
        发送信息
        """

        pass


def _recv(sk):
    """
    接受消息

    返回一个元组：(True or False, 分割后的信息列表)
    """

    try:
        data = [i.decode(u"utf8") for i in sk.recv(1024).split(b"\r\n") if i]
        assert data
        return (True, data)

    except AssertionError:  # SMTP 返回空信息
        return (False, [u"recv empty answer"])

    except Exception as e:  # SMTP 返回信息时出错
        return (False, [u"recv error: "+str(e)])


def _connect(SMTP_addr, port, timeout,):
    """
    建立 socket 连接
    """

    sk = socket.socket()
    sk.settimeout(timeout)

    try:
        sk.connect((SMTP_addr, port))
    except Exception as e:
        return (0, str(e))

    status, data = _recv(sk)
    if status and "220" not in data[-1]:  # 检查连接，成功的话会返回 220 状态码
        status = False

    return (status, data[-1], sk)


class SpamEmail:  # 伪造邮件
    def __init__(self, to_addr, from_addr, port=25, timeout=10):
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.port = port
        self.timeout = timeout
        self.SMTP_addr = ""

    def DNSQuery(self):
        self.SMTP_addr = _dns_query(self.to_addr)

    def Connect(self):
        if not self.SMTP_addr:
            return False

        status, data, self.sk = _connect(self.SMTP_addr, port=25, timeout=10)

    def Send(self, msg):
        for result in msg.split(u"\r\n"):
            try:
                self.sk.sendall((result+u"\r\n").encode("utf8"))
                Print(result)
            except Exception as e:
                Print(str(e))
                return False
        return True

    def Recv(self):
        return _recv(self.sk)

    def Attack():
        self.DNSQuery()
        self.Connect()


class EmailBomb:  # 邮件炸弹
    def __init__(self):
        pass


def _dns_query(to_addr):  # ok
    """
    解析收件地址的 dns mx 记录
    """

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 3

    Print(u"query MX of DNS for %s" % to_addr)

    try:
        SMTP_addr = b'.'.join(dns.resolver.query(
            to_addr[to_addr.find(u"@")+1:], u'MX')[0].exchange.labels).decode(u"utf8")
        assert SMTP_addr != u""
    except Exception as e:
        Print(u"query MX of %s failed: " % to_addr + str(e))
        return False

    Print(u"success")
    return SMTP_addr


def PutColor(string, color):  # ok
    """
    加点颜色~
    """
    colors = {
        u"gray": "2",
        u"red": "31",
        u"green": "32",
        u"yellow": "33",
        u"blue": "34",
        u"pink": "35",
        u"cyan": "36",
        u"white": "37",
    }

    return u"\033[40;1;%s;40m%s\033[0m" % (colors[color], string)


def ShowLogo():  # ok
    """
    打印 logo，同时清空终端的输出
    """
    print("\033c\033[?25l")
    print(LOGO)


def Print(msg):
    print(msg)



# -------------------------------- 全局变量 ------------------------
LOGO = """
\033[40;1;40m ███████╗     ██╗  ██╗\033[0m
\033[40;1;40m ██╔════╝     ██║  ██║ \033[40;1;33;40mTr0y\033[0m\033[0m
\033[40;1;40m █████╗       ███████║ \033[0m
\033[40;1;40m ██╔══╝       ██╔══██║ \033[40;1;33;40mv2.0\033[0m\033[0m
\033[40;1;40m ███████╗     ██║  ██║\033[0m
 ╚══════╝\033[40;1;32;40mmail\033[0m ╚═╝  ╚═╝\033[40;1;32;40macker\033[0m
"""
# ----------------------------------------------------------------
