# -*- coding: utf-8 -*-

from time import sleep
import random
import threading
import argparse
import signal
import sys
import os
import do_not_use_it

parser = argparse.ArgumentParser()
parser.add_argument(u"-faddr", u"--from_address",
                    help=u"fake-from-address", required=True)

parser.add_argument(u"-taddr", u"--to_address",
                    help=u"the address you want to delivery", required=True)

parser.add_argument(u"-s", u"--subject",
                    help=u"email's subject", required=True)

parser.add_argument(u"-b", u"--body",
                    help=u"email's body(content)", required=True)

parser.add_argument(u"-tnum", u"--threads_num",
                    help=u"how many threads you want (default is 1)", default=1, type=int)

parser.add_argument(u"-v", u"--verbose",
                    help=u"verbose level (choice in [0, 1, 2, 3])", default=-1, type=int)

parser.add_argument(u"-c", u"--crazy_mode",
                    help=u"Keep sending fake-email (default is False ** Use with caution **)", action='store_true', default=False)


args = parser.parse_args()

succ_num = failed_num = 0
quit_flag = print_flag = 1
ver = -1
from_addr = args.from_address
to_addr = args.to_address
subject = args.subject.decode("utf8") if vars(str).get("decode") else args.subject
body = (args.body.decode(
    "utf8") if vars(str).get("decode") else args.body).replace("\\n", "\r\n")
threads_num = args.threads_num if args.threads_num > 0 else 1
verbose = args.verbose
crazy_mode = args.crazy_mode
threads_alive = [1]*threads_num
Data = [do_not_use_it.PutColor('0', "cyan")]*threads_num
Lock = threading.Lock()

do_not_use_it.ShowLogo()

ea = do_not_use_it.SpamEmail(to_addr, from_addr)


ea.DNSQuery()
print u"connect to %s:%s " % (ea.SMTP_addr, str(ea.port))
print ea.Connect()

print ea.Send("ehlo anti-anti-spam")
status, data = ea.Recv()
if not status:
    sys.exit("Over")
else:
    for d in data:
        print d

print "\033[?25h"
