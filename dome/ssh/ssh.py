
#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import paramiko
ip,port = '192.168.123.158','22'
username,password = 'root','123'

# 创建ssh对象
ssh = paramiko.SSHClient()
# 解决ssh第一次连接,认证问题
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(ip,port,username,password)

# 执行命令
stdin,stdout,stderr = ssh.exec_command('ping 192.168.123.1')     # stdin 标准输入,  stdout 命令执行的结果， stderr 命令执行错误的结果

# 获取命令结果
ret = stdout.read()
if ret:
    print(ret.decode('utf-8').strip())
else:
    print("命令执行失败")
    print(stderr.read().decode('utf-8').strip())

# 关闭连接
ssh.close()

# 执行结果：
b'docker-server\n'   # byte 类型,需要decode转码

