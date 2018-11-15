# encoding: utf8
import curses
import curses.textpad
import os


class Screen(object):
    UP = -1
    DOWN = 1

    LEFT = -1
    RIGHT = 1

    def __init__(self, items):
        """ Initialize the screen window

        Attributes
            window: A full curses screen window

            width: The width of `window`
            height: The height of `window`

            max_lines: Maximum visible line count for `result_window`
            top: Available top line position for current page (used on scrolling)
            bottom: Available bottom line position for whole pages (as length of items)
            current: Current highlighted line number (as window cursor)
            page: Total page count which being changed corresponding to result of a query (starts from 0)

            ┌--------------------------------------┐
            |1. Item                               |
            |--------------------------------------| <- top = 1
            |2. Item                               |
            |3. Item                               |
            |4./Item///////////////////////////////| <- current = 3
            |5. Item                               |
            |6. Item                               |
            |7. Item                               |
            |8. Item                               | <- max_lines = 7
            |--------------------------------------|
            |9. Item                               |
            |10. Item                              | <- bottom = 10
            |                                      |
            |                                      | <- page = 1 (0 and 1)
            └--------------------------------------┘

        Returns
            None
        """

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

        curses.def_prog_mode()
        curses.noecho()
        curses.cbreak()

        """
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)

        self.current = curses.color_pair(2)
        """

        #self.height, self.width = self.window.getmaxyx()

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

            elif ch == curses.ascii.ESC:
                break

        # self.window.erase()
        # self.window.endwin()

    def display(self):
        """Display the items on window"""
        self.window.erase()
        #self.current = 0
        for idx, item in enumerate(
            self.items[self.top:
                       self.top + self.max_lines]
        ):
            # Highlight the current cursor line

            if idx == self.current:
                data = (item+"<=%d" % self.current)
            else:
                data = item

            # 1. 字符串长度超出默认 win 的长度，需要扩大 win
            # 2. 终端宽度被调整，需要 resize

            if self.width < len(data) or self.window.getmaxyx()[1] != self.width:
                self.window.resize(self.height, len(data)+5)
                self.height, self.width = self.window.getmaxyx()

            # try:
            self.window.addstr(idx, 0, data[self.hori_len:])  # , curses.color_pair(1))
            # except Exception:
            #    self.window.resize(self.height, len(data)+5)
            #    self.height, self.width = self.window.getmaxyx()
            #    self.window.addstr(idx, 0, data[self.hori_len:])
#
        self.window.refresh()

    def scroll(self, direction, horizontal=False):
        """Scrolling the window when pressing up/down arrow keys"""

        if horizontal:
            if (direction == self.LEFT) and self.hori_len > 0:
                self.hori_len -= 1

            elif (direction == self.DOWN):
                self.hori_len += 1
        else:
            # Up direction scroll overflow
            # current cursor position is 0, but top position is greater than 0
            if (direction == self.UP) and (self.top > 0):
                self.top += direction

            # Down direction scroll overflow
            # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
            elif (direction == self.DOWN) and (self.top + self.max_lines < self.bottom):
                self.top += direction


items = ['{}. temItemtemItemItemItemItemItemItemItemItemItemItemItem'.format(
    num) for num in range(50)]
Screen(items)

# ItemItemItemItemItemItemItemIItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemtemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItemItem
