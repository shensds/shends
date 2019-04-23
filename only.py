#coding=utf-8
import time
import socket 



def only(port,timeout,flush = 3):
    """
    port    监听端口号
    timeout 设置等待时间
    """
    global hyf_suo 
    while(1):
        if timeout<0:break
        try:
            hyf_suo = socket.socket()
            hyf_suo.bind(("127.0.0.1",port))
        except OSError:
            print("已有另一个脚本正在执行，等待{}秒".format(timeout))
            time.sleep(flush)
            timeout -= flush
            



only(438,7,1)
for i in range(1000):
    print(1000 - i)
    time.sleep(1)