# encoding: utf8
import curses
import threading
import time
import random


class CtrlC(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        try:
            self._func()
        except KeyboardInterrupt:
            pass


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
        self.items = ITEMS
        self.bottom = len(self.items)
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
        """Display the ITEMS on window"""
        self.window.erase()

        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines]):
            data = item.data

            tmp_height, tmp_width = self.window.getmaxyx()
            '''
            self.width > len(data) > tmp_width: self.width √
            self.width > tmp_width > len(data): self.width

            tmp_width > self.width > len(data): tmp_width
            tmp_width > len(data) > self.width: tmp_width √

            len(data) > tmp_width > self.width: len(data)
            len(data) > self.width > tmp_width: len(data) √
            '''

            # 字符串长度超出默认 win 的长度，需要 resize
            if self.width < len(data):
                self.width = len(data)
                self.window.resize(self.height, self.width)

            # 终端宽度被调整，需要 resize
            if tmp_width != self.width:
                self.width = max(self.width, tmp_width)
                self.window.resize(self.height, self.width)

            '''
            这样是不行的，别问我为啥 :D
            maxwidth = max(self.width, tmp_width, len(data))
            if maxwidth != self.width or 1:
                self.width = maxwidth
                self.window.resize(self.height, self.width)
            '''

            # 终端高度被调整，需要 resize
            if tmp_height != self.height:
                self.max_lines = min(self.height, tmp_height)
                self.height = max(self.height, tmp_height)
                self.window.resize(self.height, self.width)
                self.top = 0

            self.window.addstr(idx, 0, data[self.hori_len:])

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

        EXIT_FLAG = 0  # screen 的线程 gg 的时候，退出 process_data


class Line:
    '''
    每一行为一个实例
    '''

    def __init__(self, id, data=""):
        self.header = "{0:{fill}{align}{length}}".format(
            "No."+str(id)+": ", length=len(str(THREADS_NUM))+5, fill=" ", align=">"
        )  # 不变的数据头。使用空格进行右对齐

        self.body = data  # 数据体，具体数据
        self.data = self.header+self.body  # 真正展示出来的数据为 数据头+数据体

    def update_body(self, data):
        '''
        更新数据体的时候也得更新真正展示出来的数据
        '''

        self.body = data
        self.data = self.header+self.body


@CtrlC
def process_data():
    '''
    处理数据
    这里更新的数据会在线程 thread_screen 中展示出来
    '''

    while EXIT_FLAG:
        ITEMS[random.randint(0, THREADS_NUM-1)].update_body("attacking...")
        time.sleep(0.5)


# ---------- 全局变量 -----------
EXIT_FLAG = 1

THREADS_NUM = 50

# 每一行的数据
ITEMS = [Line(num, "starting...") for num in range(THREADS_NUM)]

# ------------------------------

"""
thread_screen = threading.Thread(target=Screen)
thread_screen.setDaemon(True)
thread_screen.start()  # 启动线程 thread_screen 用于展示数据
"""

thread_data = threading.Thread(target=process_data)
thread_data.setDaemon(True)
thread_data.start()  # 启动线程 thread_data 用于处理数据

Screen()

print "Bye~"
