# -*- coding:utf-8  -*-

#!/usr/bin/python3
 
import subprocess
import os




def get_status_output(cmd):
    """Exec command Returns the status and output after execution"""
    pipe = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = pipe.communicate(input=b'y')[0]
    try:
        out = out.decode('UTF-8')
    except UnicodeDecodeError:
        out = out.decode('gbk', errors='ignore')

    try:
        pipe.kill()
    except OSError:
        pass
    return pipe.returncode, out







import subprocess
import sys


# 常用编码
GBK = 'gbk'
UTF8 = 'utf-8'

# 解码方式，一般 py 文件执行为utf-8 ，cmd 命令为 gbk
current_encoding = GBK


popen = subprocess.Popen(['ping', 'www.baidu.com'],
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE,
                         bufsize=1)

# 重定向标准输出
while popen.poll() is None:         # None表示正在执行中
    r = popen.stdout.readline().decode(current_encoding)
    sys.stdout.write(r)                    # 可修改输出方式，比如控制台、文件等

# 重定向错误输出
if popen.poll() != 0:                      # 不为0表示执行错误
    err = popen.stderr.read().decode(current_encoding)
    sys.stdout.write(err)                 # 可修改输出方式，比如控制台、文件等














obj = subprocess.Popen(["python3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
obj.stdin.write(b'pwd\n')
# obj.stdin.write(b'wocao \n')
# obj.stdin.write(b'print(3) \n')
out,err = obj.communicate()
print("\n\n\n\n")
print(out.decode())
print("err")
print(err)
print("\n\n\n\n")
