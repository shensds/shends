#!C:\python37\python.exe
# -*- coding: UTF-8 -*-
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import logging
import socket
 
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
def ftp_server():
    #实例化虚拟用户，这是FTP验证首要条件
    authorizer = DummyAuthorizer()
    
    #添加用户权限和路径，括号内的参数是(用户名， 密码， 用户目录， 权限)
    # 读权限 ：
    # e	改变文件目录
    # l	列出文件
    # r	从服务器接收文件
    # 写权限 ：
    # a	文件上传
    # d	删除文件
    # f	文件重命名
    # m	创建文件
    # w	写权限
    # M	文件传输模式(通过FTP设置文件权限 )
    authorizer.add_user('admin', 'admin', 'F:\\', perm='elradfmw')

    #添加匿名用户 只需要路径
    #authorizer.add_anonymous('/home/')

    #下载上传速度设置
    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = 300*1024 #下载速度 300kb/s
    dtp_handler.write_limit = 300*1024#上传速度  300kb/s

    #初始化ftp句柄
    handler = FTPHandler
    handler.authorizer = authorizer
    #日志记录
    #logging.basicConfig(filename="pyftp.log", level=logging.INFO)
    #欢迎信息
    handler.banner = 'Welcome to python ftp'
    #添加被动端口范围
    handler.passive_ports = range(2000,2200)

    #监听ip 和 端口
    ip = get_host_ip()
    server = FTPServer((ip, "2121"), handler)

    #最大连接数
    server.max_cons = 2
    server.max_cons_per_ip = 2
    
    #开始服务
    print('开始服务')
    server.serve_forever()
if __name__ == "__main__":

    ftp_server()
    
