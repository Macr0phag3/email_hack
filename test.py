# -*- coding: utf-8 -*-

import curses
import time
import threading


class Pad:
    def __init__(self, length, width):
        self.length = length  # 长度
        self.width = width  # 宽度

        self.length_show = self.length  # 展现的长度
        self.width_show = self.width/3  # 展现的宽度

        self.x = 0
        self.y = 0  # lake max y :)

        curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.init_pad()

    def init_pad(self):
        self.the_pad = curses.newwin(self.length, self.width)
        #self.the_pad = curses.newpad(self.length, self.width)

        self.the_pad.keypad(1)

        show_thread = threading.Thread(target=self.show)
        show_thread.start()

    def refresh(self):
        # self.x: 矩形左上角的 x 坐标（即 @ 的 x 坐标）
        # self.y: 矩形左上角的 y 坐标（即 @ 的 y 坐标）
        # 0: 起始的 x 坐标
        # 0: 起始的 y 坐标
        # self.width_show: 结束的 x 坐标
        # self.length: 结束的 y 坐标
        #
        # 示例
        # **@@@@@******
        # **@@@@@******
        # **@@@@@******
        # *************
        #
        # 左上角的 @ 所在的坐标为：self.x, self.y，这里即为 (2, 0)
        # 如果想刷新上面所有的 @，则后面 4 个参数应写为：()
        self.the_pad.refresh()  # self.x, self.y, 0, 0, self.width, self.length)

    def draw(self, x, y, string):
        """
        print len(string)
        self.length = 10000
        self.the_pad.resize(self.length, self.width)
        self.refresh()
        """
        print len(string)
        if len(string) > self.length:
            self.length = len(string)
            self.the_pad.resize(self.length, self.width)
            self.refresh()

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


pad = Pad(100, 10)

for i in range(200):
    pad.draw(i, 0, str(i)*100)
    time.sleep(0.5)
    break
