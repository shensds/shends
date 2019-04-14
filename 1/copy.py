# -*- coding: utf-8 -*-
import os

def rm(dir):
    #windows系统
    if os.name == "nt":
        #文件用del删除
        if os.path.isfile(dir):
            out = os.system("del /f /q {}".format(dir))
            return out
        #目录用rd删除
        while(1):
            out = os.system("rd /s /q {}".format(dir))
            if not (out ==0 and os.path.isdir(dir)):break
    #linux系统
    elif os.name == "posix":
        if dir == "/":return False
        while(1):
            out = os.system("rm -rf {}".format(dir))
            if not (out ==256 and os.path.isdir(dir)):break
    return out

def cp(src,dst):
    if os.name == "nt":
        #文件用copy拷贝
        if os.path.isfile(src) and dst[-1] !="\\":
            if not os.path.isdir(os.path.dirname(dst)):
                os.makedirs(os.path.dirname(dst))
            out = os.system("copy /y {} /b {} /b".format(src,dst))
            return out
        out = os.system("xcopy /e /q /r /i /y {} {}".format(src,dst))
    elif os.name == "posix":
        if not os.path.isdir(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        if os.path.isdir(src) and os.path.isdir(dst):
            if src[-1]!="/":src = src + "/*"
            else:src = src + "*"
        out = os.system("cp -r {} {}".format(src,dst))
    return out

if "__name__" == "__main__":
    pass
