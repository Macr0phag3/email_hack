# -*- coding: utf-8 -*-

import curses
import time
import threading


class Pad:
    def __init__(self, length, width):
        self.length = length  # 长度
        self.width = width  # 宽度

        self.width_show = self.width/3  # 展现的宽度

        self.x = 0
        self.y = 0  # lake max y :)

        curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.initscr()

    def initscr(self):

        self.the_pad = curses.newpad(self.length, self.width)

        self.the_pad.keypad(1)

        show_thread = threading.Thread(target=self.show)
        show_thread.start()

    def refresh(self):
        self.the_pad.refresh(self.x, self.y, 0, 0, self.width_show, self.length)

    def draw(self, x, y, string):
        try:
            self.the_pad.addstr(x, y, string)
        except curses.error:
            return False

        self.refresh()

        """
        if x > self.width_show:
            self.x += 1
        """

    def show(self):
        while 1:
            cmd = self.the_pad.getch()
            if cmd == curses.KEY_DOWN:
                if self.x < self.width:
                    self.x += 1
            elif cmd == curses.KEY_UP:
                if self.x > 0:
                    self.x -= 1
            else:
                break

            self.refresh()

        curses.endwin()


pad = Pad(100, 50)

for i in range(200):
    pad.draw(i, 0, str(i))
    time.sleep(0.1)
