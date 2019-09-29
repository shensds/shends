#!/usr/bin/python3
# 文件名：server.py
import socket
import subprocess
import sys

def exec_cmd(cmd):
    cmd_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cmd_echo = cmd_process.stdout.read()
    cmd_process.stdout.close()
    sts = cmd_process.wait()
    return sts, cmd_echo.strip()

# 创建 socket 对象
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()
port = 9999

# 绑定端口号
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(5)

while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()

    print("连接地址: %s" % str(addr))
    cmd = clientsocket.recv(1024)
    print(cmd)
    ret,text = exec_cmd(cmd.decode())
    print(text)
    clientsocket.send(text)
    print("发送成功")
    clientsocket.close()