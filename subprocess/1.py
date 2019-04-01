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










# class Shell(object) :
    # def runCmd(self, cmd) :
        # res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # sout ,serr = res.communicate() 
        # return res.returncode, sout, serr, res.pid

# shell = Shell()

# returncode, sout, serr, pid = shell.runCmd("ifconfig")

# print(returncode)
# print(sout.decode())
# print(serr)
# print(pid)


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
