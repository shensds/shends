#!/usr/bin/python3
# -*- coding:utf-8  -*-
#mysql版本8.0，脚本请放在mysql根目录下运行
import os
import re
import subprocess

def get_status_output(cmd):
    """Exec command Returns the status and output after execution"""
    pipe = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out ,err = pipe.communicate(input=b'y')
    try:
        out = out.decode('UTF-8')
    except UnicodeDecodeError:
        out = out.decode('gbk', errors='ignore')

    try:
        pipe.kill()
    except OSError:
        pass
    return out, err

#my.ini为mysql的配置文件
my_ini = '''
[mysqld]
# 设置3306端口
port=3306
# 设置mysql的安装目录
basedir=D:\\www\\mysql-8.0.15-winx64
# 设置mysql数据库的数据的存放目录
datadir=D:\\www\\mysql-8.0.15-winx64\\data
# 允许最大连接数
max_connections=200
# 允许连接失败的次数。这是为了防止有人从该主机试图攻击数据库系统
max_connect_errors=10
# 服务端使用的字符集默认为UTF8
character-set-server=utf8
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
[mysql]
# 设置mysql客户端默认字符集
default-character-set=utf8
[client]
# 设置mysql客户端连接服务端时默认使用的端口
port=3306
default-character-set=utf8
'''
#写入配置文件
with open("my.ini","w+") as fp:
    fp.write(my_ini)

MyFile = os.path.realpath(__file__)
MyPath = os.path.dirname(MyFile)
print(MyFile)
print(MyPath)
os.chdir(MyPath+"\\bin")
#setx PATH "%PATH%; C:\XXX\" /M
#初始化，获取临时密码

out,err = get_status_output("mysqld --initialize --user=mysql --console")
re.search("error",out)
with open("install.log","wb+") as fp:
    fp.write(out)

out,err = get_status_output("mysqld -install")






