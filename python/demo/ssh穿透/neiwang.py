# -*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
from threading import Thread
import socket


host = "192.168.123.229"
port = 3838
w = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
w.connect((host, port))
logging.info("%s:%s链接成功"%(host,port))
port = 22
host = "127.0.0.1"
n = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
n.connect((host, port))


def aaa():
    while True:
        msg = w.recv(1)
        n.send(msg)

def bbb():
    while True:
        cmd = n.recv(1)
        w.send(cmd)
        
a = Thread(target = aaa)
b = Thread(target = bbb)
a.start()
b.start()
a.join()
b.join()

