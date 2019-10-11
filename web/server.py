import logging
from threading import Thread
import os
import importlib
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
import socket

myfile = os.path.realpath(__file__)
mypath = os.path.dirname(myfile)
import py




s = socket.socket()
ip = py.get_host_ip()
ip = (ip, 8001)
logging.info("绑定地址：%s"%str(ip))
s.bind(ip)
s.listen()







def start(conn,data):
    print("\n\n")
    dir, file, args = py.prase_date(data)
    if ".py" in file:
        py.py(conn,dir, file, args)
        return
    header,response = py.get_response(dir, file, args)
    conn.send(header)
    conn.send(response)
    conn.close()

while 1:
    importlib.reload(py)
    conn, _ = s.accept()
    data = conn.recv(8096)
    thread = Thread(target= start,args=(conn,data))
    thread.start()
