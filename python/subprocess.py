# -*- coding:utf-8  -*-
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


def exec_cmd(cmd):
    cmd_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cmd_echo = cmd_process.stdout.read()
    cmd_process.stdout.close()
    sts = cmd_process.wait()
    try:
        cmd_echo = cmd_echo.decode('UTF-8')
    except UnicodeDecodeError:
        cmd_echo = cmd_echo.decode('gbk', errors='ignore')
    if int(platform.python_version().split('.')[0]) < 3:
        if platform.system().lower() == 'windows':
            cmd_echo = cmd_echo.encode('gbk', errors='ignore')
        else:
            cmd_echo = cmd_echo.encode('UTF-8', errors='ignore')
    return sts, cmd_echo.strip()
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
