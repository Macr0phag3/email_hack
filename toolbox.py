# -*- coding: utf-8 -*-


def put_color(string, color):
    colors = {
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "pink": "35",
        "cyan": "36",
        "white": "37",
    }
    return "\033[40;1;%s;40m%s\033[0m" % (colors[color], string)
