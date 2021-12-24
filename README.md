![logo](https://raw.githubusercontent.com/Macr0phag3/email_hack/master/pics/Logo.png)

## 项目介绍
using python to create a fake-email & email-bomb!

利用 Python 伪造电子邮件发件人以及制造电子邮件炸弹

（仅限学术交流，用于非法用途概不负责）

You can come to [my blog](https://www.tr0y.wang/2018/09/26/email-hacker/) or [freebuf](http://www.freebuf.com/sectool/184555.html) to get more details.

我的[博客](https://www.tr0y.wang/2018/09/26/email-hacker/) 以及 [freebuf](http://www.freebuf.com/sectool/184555.html) 均有详细的原理说明，有兴趣的话可以去看看。

## 特性
1. Python 实现，可以轻松订制
2. 每封邮件都加入了随机化的字符串，逃逸一些基础的检测
3. 利用类似长连接的方式提高了轰炸的效率
4. 详细的原理说明

## 快速开始
### Dependencies/依赖
`pip install dnspython`

**OS**
- [x] Unix
- [x] Linux

**Python version**
- [x] Py2.x
- [x] Py3.x

### 说明书
GIF 演示

- `python email_hacker.py -faddr hr@xx.com -taddr xxxxxx@163.com -s "[打码]世界 2019 校园招聘" -b "同学你好\n感谢你对[打码]世界校园招聘的关注，面试时间暂定为 9月20日 下午两点。如有疑问欢迎邮件交流~\n在茫茫宇宙中，在浩瀚银河里，有一个可以任你挥洒的世界，大家都抱着纯粹初心背负梦想前行，在这里，激情无限，跟志同道合的伙伴热血拼搏。在这里，秉持热爱，把梦想变成现实。在这里，精益求精，定义下一代未知的惊喜！"`
![no_argv](https://raw.githubusercontent.com/Macr0phag3/email_hack/master/pics/no_argv.png)

- `python email_hacker.py -faddr hr@xx.com -taddr xxxxxx@163.com -v1 -tnum 2 -c -s "[打码]世界 2019 校园招聘" -b "同学你好\n感谢你对[打码]世界校园招聘的关注，面试时间暂定为 9月20日 下午两点。如有疑问欢迎邮件交流~\n在茫茫宇宙中，在浩瀚银河里，有一个可以任你挥洒的世界，大家都抱着纯粹初心背负梦想前行，在这里，激情无限，跟志同道合的伙伴热血拼搏。在这里，秉持热爱，把梦想变成现实。在这里，精益求精，定义下一代未知的惊喜！"`
![tnum2_v1](https://raw.githubusercontent.com/Macr0phag3/email_hack/master/pics/tnum2_v1.gif)

- `python email_hacker.py -faddr hr@xx.com -taddr xxxxxx@163.com -tnum 5 -c -s "[打码]世界 2019 校园招聘" -b "同学你好\n感谢你对[打码]世界校园招聘的关注，面试时间暂定为 9月20日 下午两点。如有疑问欢迎邮件交流~\n在茫茫宇宙中，在浩瀚银河里，有一个可以任你挥洒的世界，大家都抱着纯粹初心背负梦想前行，在这里，激情无限，跟志同道合的伙伴热血拼搏。在这里，秉持热爱，把梦想变成现实。在这里，精益求精，定义下一代未知的惊喜！"`
![tnum5_c](https://raw.githubusercontent.com/Macr0phag3/email_hack/master/pics/tnum5_c.gif)

使用 ctrl+c 终止程序

参数:

```
  -h, --help            输出帮助信息

  -faddr FROM_ADDRESS, --from_address FROM_ADDRESS
                        伪造的来源邮件地址

  -taddr TO_ADDRESS, --to_address TO_ADDRESS
                        接收方的邮件地址

  -s SUBJECT, --subject SUBJECT
                        邮件主题

  -b BODY, --body BODY  邮件正文

  -tnum THREADS_NUM, --threads_num THREADS_NUM
                        多线程的线程数，默认为 1

  -v VERBOSE, --verbose VERBOSE
                        输出信息的详细程度，默认由代码自动选择，可选为 0, 1, 2, 3

  -c CRAZY_MODE, --crazy_mode CRAZY_MODE
                        长连接模式，谨慎使用，默认为False
```

### Cookbook
ctrl+c to stop

using `python email_hacker.py -h` to get help
:P

## Update/更新
- v1.0: 基本的发送，伪造功能
- v2.0:
  - 增加 verbose 为4个级别：0、1、2、3. 2018.10.01 10:10 AM
  - 更改 crazy_mode 的输出为固定行形式. 2018.10.01 17:10 AM
  - 统一代码形式. 2018.10.02 23:10 AM
  - 修复若干个 bug. ~~2018.10.02 23:10 AM~~ 2018.11.2 17:23:03
  - 优化固定行输出方案. 2018.10.04 11:10 AM

## TODO/待办
- [x] 优化固定行输出时，单行内容放不下导致输出混乱的问题。(超出命令行长度的字符将被省略输出)。
- [x] readme 增加动图演示
- [x] 修改一下 `--help` 以及参数的说明
- [x] 加个 logo
- [x] 不硬编码邮件内容
- [x] 随机邮件内容
- [x] 为 crazy_mode 增加一个级别的 verbose
- [x] 将单线程模式也开设一个线程，主进程不再负责具体任务，以便统一代码形式。
- [ ] ~弃用 python-dns 自己解析~
- [x] 重构代码，简化之。（作为练习设计模式的实验品）
  - [x] 分离 CLI 与邮件功能. 2018.11.14 16:54:34
  - [x] 先画一个 CLI. 2018.11.16 00:15:42
  - [x] 优化一下邮件功能，准备与 CLI 对接.
    - [x] FakeEmail. 2018.11.18 14:54:00
    - [x] EmailBomb. 2018.11.18 16:00:39
- [x] CLI 版本 大致完成，不打算进一步完善。功能有限，仅用于练习 curses. 2018.11.25 12:22:04
- [x] 后续可能会出一个 GUI 版本.

## 其他
<img src="https://clean-1252075454.cos.ap-nanjing.myqcloud.com/20200528120800990.png" width="500">

[![Stargazers over time](https://starchart.cc/Macr0phag3/email_hack.svg)](https://starchart.cc/Macr0phag3/email_hack)
