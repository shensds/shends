#!/usr/bin/python3
# -*- coding:utf-8  -*-
#mysql版本8.0，脚本请放在mysql根目录下运行
import os
import re
import subprocess
import configparser
MyFile = os.path.realpath(__file__)
MyPath = os.path.dirname(MyFile)
def readCfg(iniFile):
    cfg = {}
    config = configparser.ConfigParser()
    config.read_file(open(iniFile))
    
    for section in config.sections():
        cfg[section] = {}
        for option in config.options(section):
            cfg[section][option] = config.get(section, option)
            #print ("cfg[%s][%s] = %s" %(section, option, config.get(section, option)))
    return cfg

def setCfg(iniFile, section, key, value):
    if not os.path.isfile(iniFile): return
    config = configparser.ConfigParser()
    config.read_file(open(iniFile))
    config.set(section, key, value)
    fp = open(iniFile, "w")
    config.write(fp)

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
# 默认使用“mysql_native_password”插件认证
default_authentication_plugin=mysql_native_password
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
# with open("my.ini","w+") as fp:
    # fp.write(my_ini)
# #修改配置文件
# setCfg("my.ini","mysqld","basedir",MyPath)
# setCfg("my.ini","mysqld","datadir",os.path.join(MyPath,"data"))

MyPathBin = os.path.join(MyPath,"bin")

# #初始化，获取临时密码
os.chdir(MyPathBin)
out,err = get_status_output("mysqld --initialize --user=mysql --console")
print(out)
re.search("error",out)
with open("install.log","wb+") as fp:
    fp.write(out.encode())

#进行服务的添加
out,err = get_status_output("mysqld -install")


#启动服务
net start mysql
mysql -u root -p 
#设置远程登录
use mysql;
select host from user where user='root';
update user set host = '%' where user ='root'
修改密码语句：
 
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '新密码';
ALTER USER root@localhost IDENTIFIED  BY '123456';
备注：8.0之前版本，忘记密码修改方法
找到bin目录：mysqld --skip-grant-tables
重新在开一个cmd窗口
找到bin目录：mysql就进入登陆状态了
5.7.22修改密码语句：update user set authentication_string=password('123456') where user='root' and host='localhost';
5.6.修改密码语句：update user set password=password('123456') where user='root' and host='localhost'; 





