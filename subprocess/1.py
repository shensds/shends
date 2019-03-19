# -*- coding:utf-8  -*-

#!/usr/bin/python3
 
import subprocess
import os
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