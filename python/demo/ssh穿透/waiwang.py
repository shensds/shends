# -*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
from threading import Thread
import socket



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 3838
host = "192.168.123.229"
serversocket.bind((host, port))
serversocket.listen(5)
n, addr = serversocket.accept()
print("连接地址: %s" % str(addr))



host = "192.168.123.229"
port = 8888
waiwang = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
waiwang.bind((host, port))
waiwang.listen(5)
w, addr = waiwang.accept()
print("连接地址: %s" % str(addr))

def aaa():
    while True:
        msg = n.recv(1)
        w.send(msg)

def bbb():
    while True:
        cmd = w.recv(1)
        n.send(cmd)
a = Thread(target = aaa)
b = Thread(target = bbb)
a.start()
b.start()
a.join()
b.join()

