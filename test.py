# encoding: utf8
import curses
import os
import threading
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
        self.items = items
        self.bottom = len(self.items)
        self.current = self.bottom - 1
        self.max_lines = curses.LINES
        self.hori_len = 0

        self.run()

    def init_curses(self):
        """Setup the curses"""
        self.window = curses.initscr()
        self.height, self.width = self.window.getmaxyx()
        self.window.keypad(True)

        curses.noecho()
        curses.cbreak()

    def put_color(self, color, bold=False):
        bold = [bold, curses.A_BOLD][bold]

        if color == "white":
            return -1

        return curses.color_pair(1) | curses.A_RIGHT

    def run(self):
        """Continue running the TUI until get interrupted"""

        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass

        os.system("printf '\e]50;ClearScrollback\a'")  # 兼容 iTerm2
        curses.endwin()

    def input_stream(self):
        """Waiting an input and run a proper method according to type of input"""
        while True:

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
        """Display the items on window"""
        self.window.erase()

        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines]):
            data = item

            # 1. 字符串长度超出默认 win 的长度，需要扩大 win
            # 2. 终端宽度被调整，需要 resize
            if self.width < len(data) or self.window.getmaxyx()[1] != self.width:
                self.window.resize(self.height, len(data)+5)
                self.height, self.width = self.window.getmaxyx()

            self.window.addstr(idx, 0, data[self.hori_len:])

        self.window.refresh()

    def scroll(self, direction, horizontal=False):
        """Scrolling the window when pressing up/down arrow keys"""

        if horizontal:
            if (direction == self.LEFT) and self.hori_len > 0:
                self.hori_len -= 1

            elif (direction == self.DOWN):
                self.hori_len += 1
        else:
            if (direction == self.UP) and (self.top > 0):
                self.top += direction

            elif (direction == self.DOWN) and (self.top + self.max_lines < self.bottom):
                self.top += direction


def create_screen():
    Screen()


def process_data():
    global items

    for i in range(10):
        items[i] += "1"
        time.sleep(1)


threads_num = 20

items = ['']*threads_num

"""
items = ["{0:{fill}{align}{length}}".format(
    "No."+str(num)+": ", length=len(str(threads_num))+5, fill=" ", align=">"
) for num in range(threads_num)]
"""

thread_screen = threading.Thread(target=create_screen)
thread_screen.start()

thread_data = threading.Thread(target=process_data)
thread_data.start()
thread_data.join()

print "Bye~"
