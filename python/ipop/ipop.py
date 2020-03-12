# -*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
from threading import Thread
import socket
import time
class common():
    def __init__(self):
        pass
        
a = common
a.CONNECT = False

def connect():
    host = a.host
    port = a.port
    while True:
        a.s_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a.s_connect.connect((host, port))
        logging.info("%s:%s链接成功"%(host,port))
        a.CONNECT = True
        while True:
            time.sleep(1)
            






def aaa(clicent):
    while True:
        msg = clicent.recv(1)
        a.s_connect.send(msg)
        time.sleep(1)

def bbb(clicent):
    while True:
        msg = a.s_connect.recv(1)
        clicent.send(cmd)


def share():
    while True:
        if a.CONNECT == True:
            host = a.SHARE_HOST
            port = a.SHARE_PORT
            a.s_share = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a.s_share.bind((host, port))
            a.s_share.listen(5)
            clicent, addr = a.s_share.accept()
            logging.info("连接地址: %s" % str(addr))
            a1 = Thread(target = aaa,args=(clicent,))
            a2 = Thread(target = bbb,args=(clicent,))
            a1.start()
            a1.join()
            # a2.start()


        else:
            time.sleep(1)
    



a.host = "192.168.123.1"
a.port = 80
a.SHARE_HOST = "0.0.0.0"
a.SHARE_PORT = 80
thread_connect = Thread(target = connect)
thread_connect.start()
thread_share = Thread(target = share)
thread_share.start()






