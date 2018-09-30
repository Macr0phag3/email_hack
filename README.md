```
███████╗     ██╗  ██╗
██╔════╝     ██║  ██║ by Tr0y
█████╗       ███████║ v2.0
██╔══╝       ██╔══██║
███████╗     ██║  ██║
╚══════╝mail ╚═╝  ╚═╝acker
```

using python to create a fake-email & email-bomb!

利用 Python 伪造电子邮件发件人以及制造电子邮件炸弹

（仅限学术交流，用于非法用途概不负责）

You can come to [my blog](https://www.tr0y.wang/2018/09/26/email-hacker/) or [freebuf](http://www.freebuf.com/sectool/184555.html) to get more details.

我的[博客](https://www.tr0y.wang/2018/09/26/email-hacker/) 以及 [freebuf](http://www.freebuf.com/sectool/184555.html) 均有详细的原理说明，有兴趣的话可以去看看。

## Dependencies
`pip install dnspython`

**OS**
- [x] Unix
- [x] Linux

**Python version**
- [x] Py2.x
- [x] Py3.x


## 说明书
使用 ctrl+c 终止程序

参数:
```
  -h, --help            输出帮助信息

  -faddr FROM_ADDRESS, --from_address FROM_ADDRESS
                        伪造的来源邮件地址

  -taddr TO_ADDRESS, --to_address TO_ADDRESS
                        接收方的邮件地址

  -tnum THREADS_NUM, --threads_num THREADS_NUM
                        多线程的线程数，默认为 1，即单线程

  -v VERBOSE, --verbose VERBOSE
                        输出信息的详细程度，默认由代码自动选择，可选为 0, 1, 2

  -c CRAZY_MODE, --crazy_mode CRAZY_MODE
                        长连接模式，谨慎使用，默认为0，可选为 0, 1
```

## Cookbook
ctrl+c to stop

using `python email_hacker.py -h` to get help
:P

## Update
- v1.0: 基本的发送，伪造
- v2.0:
  - 增加 verbose 为4个级别：0、1、2、3
  - 更改 crazy_mode 的输出为固定行形式
  - 统一代码形式
  - 修复若干个 bug

## TODO
- [ ] 修改一下 `--help` 以及参数的说明
- [x] 加个 logo
- [ ] 不硬编码邮件内容
- [ ] 随机邮件内容
- [x] 为 crazy_mode 增加一个级别的 verbose
- [x] 将单线程模式也开设一个线程，主进程不再负责具体任务，以便统一代码形式。
- [ ] ~~弃用 `dnspython` 自己写~~
