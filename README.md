using python to create fake email & email bomb!

## requires
`pip install dnspython`

Supported: Unix, Linux, Py2.x, Py3.x

Unknown: Windows


## 说明书
（使用 ctrl+c 终止程序，按一次就够了

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
（ctrl+c **once** to stop,

using `python email_hacker.py -h` to get help
:P


## TODO
- [ ] 不硬编码邮件内容
- [ ] 随机邮件内容
- [ ] 为 crazy_mode 增加一个级别的 verbose
- [ ] 将单线程模式也开设一个线程，主进程不再负责具体任务，以便统一代码形式。
- [ ] ~~弃用 `dnspython` 自己写~~
