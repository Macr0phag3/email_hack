# -*- coding: utf-8 -*-

import EmailBomb
import threading
import curses
import time
import locale
locale.setlocale(locale.LC_ALL, '')


class Screen:
    UP = -1
    DOWN = 1

    LEFT = -1
    RIGHT = 1

    COLORS = {
        "red": 1,
        "yellow": 2,
        "cyan": 3,
        "green": 4,
        "white": 5,
        "gray": 6,
    }

    def __init__(self):
        self.too_small = False

        self.init_curses()

        self.top = 0
        self.bottom = len(CLIENTS)
        self.max_lines = curses.LINES-len(LOGO)

        self.hori_len = 0
        self.EXIT_FLAG = 0

    def init_curses(self):
        """Setup the curses"""
        self.window = curses.initscr()
        self.height, self.width = self.window.getmaxyx()
        if self.width < 60:
            self.too_small = True
            return

        self.window.keypad(True)
        # self.window.nodelay(True)

        curses.noecho()
        curses.curs_set(False)
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def put_color(self, color, bold=True):
        bold = [bold, curses.A_BOLD][bold]

        return {
            "red": curses.color_pair(1),
            "yellow": curses.color_pair(2),
            "white": curses.color_pair(3),
            "green": curses.color_pair(4),
        }[color] | bold

    def input_stream(self):
        """Waiting an input and run a proper method according to type of input"""

        while not self.EXIT_FLAG:
            ch = self.window.getch()

            if ch == curses.KEY_UP:
                self.scroll(self.UP)

            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)

            elif ch == curses.KEY_LEFT:
                self.scroll(self.LEFT, horizontal=True)

            elif ch == curses.KEY_RIGHT:
                self.scroll(self.RIGHT, horizontal=True)

            elif ch == ord("q"):
                self.EXIT_FLAG = 1

    def display(self):
        """Display the CLIENTS on window"""
        condition = 1
        while condition:
            try:
                self.window.erase()
                if self.EXIT_FLAG:
                    condition = any([client.running for client in CLIENTS])
                    for client in CLIENTS:
                        if not client.exit_flag:
                            client.exit_flag = self.EXIT_FLAG
                        else:
                            if client.running:
                                client.status = [(client.status_header, "exiting", "yellow")]
                            else:
                                client.status = [(client.status_header, "exited", "red")]

                for idx, item in enumerate(LOGO+CLIENTS[self.top:self.top + self.max_lines]):
                    data = item.status[0] if len(item.status) == 1 else item.status.pop()

                    len_data = len(data[0]+data[1])
                    tmp_height, tmp_width = self.window.getmaxyx()
                    '''
                    self.width > len(data) > tmp_width: self.width √
                    self.width > tmp_width > len(data): self.width

                    tmp_width > self.width > len(data): tmp_width
                    tmp_width > len(data) > self.width: tmp_width √

                    len(data) > tmp_width > self.width: len(data)
                    len(data) > self.width > tmp_width: len(data) √

                    这样是不行的，别问我为啥 :D
                    maxwidth = max(self.width, tmp_width, len(data))
                    if maxwidth != self.width or 1:
                        self.width = maxwidth
                        self.window.resize(self.height, self.width)
                    '''

                    # 字符串长度超出默认 win 的长度，需要 resize
                    if self.width < len_data:
                        self.width = len_data
                        self.window.resize(self.height, self.width)
                        time.sleep(1)

                    # 终端宽度被调整，需要 resize
                    if tmp_width != self.width:
                        self.width = max(self.width, tmp_width)
                        self.window.resize(self.height, self.width)
                        time.sleep(1)

                    # 终端高度被调整，需要 resize
                    if tmp_height != self.height:
                        self.max_lines = min(self.height, tmp_height)
                        self.height = max(self.height, tmp_height)
                        self.window.resize(self.height, self.width)
                        self.top = 0
                        time.sleep(1)

                    try:
                        self.window.addstr(idx, 0, data[0], self.put_color("white"))
                        tmp_length = len(data[0])
                        self.window.addstr(idx, tmp_length, data[1][self.hori_len:], self.put_color(data[2]))
                    except Exception:
                        self.EXIT_FLAG = 1
                        break
                        # self.window.addstr(idx, 0, "too small", self.put_color("white"))

                self.window.refresh()

                # time.sleep(0.5)

            except KeyboardInterrupt:
                self.EXIT_FLAG = 1

    def scroll(self, direction, horizontal=False):
        '''
        垂直滚动与水平滚动
        '''

        if horizontal:  # 水平滚动
            if (
                # self.hori_len > 0：如果已经到最左边，就不滚动了
                direction == self.LEFT and self.hori_len > 0
            ) or (
                # 右边不限制
                direction == self.RIGHT
            ):
                self.hori_len += direction

        else:  # 垂直滚动
            if (
                direction == self.UP and self.top > 0
            ) or (
                direction == self.DOWN and self.top + self.max_lines < self.bottom
            ):
                self.top += direction

    def run(self):
        """Continue running the TUI until get interrupted"""

        self.display()

        # 兼容 iTerm2
        # os.system("printf '\e]50;ClearScrollback\a'")
        # 兼容个屁 :D

        curses.endwin()

        # screen 的线程结束的时候
        # 通知 process_data 结束


class LOGOLine:
    def __init__(self, data):
        self.status = [(data, "", "red")]


# ---------- 全局变量 -----------


LOGO = [
    LOGOLine(i) for i in [
        "",
        "███████╗     ██╗  ██╗",
        "██╔════╝     ██║  ██║",
        "█████╗       ███████║",
        "██╔══╝       ██╔══██║",
        "███████╗     ██║  ██║",
        "╚══════╝mail ╚═╝  ╚═╝acker",
        "",
    ]
]

THREADS_NUM = 30

CLIENTS = [
    EmailBomb.EmailBomb(
        id=id,
        from_addr="hr@361.com",
        to_addr="@163.com",
    ) for id in range(THREADS_NUM)
]  # 创建攻击 client
# ------------------------------
sc = Screen()  # 对接 CLI 展示数据


if sc.too_small:
    print("too small")
else:
    for client in CLIENTS:
        thread = threading.Thread(target=client.attack, args=("hello! my friend!", "hr: you got it!",))
        thread.setDaemon(True)
        thread.start()  # 启动攻击 client

    t = threading.Thread(target=sc.input_stream)
    t.start()

    sc.run()
