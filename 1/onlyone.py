# coding: utf-8
import os

import time

def only():
    pid_file = "d:\\tmp.txt"
    if os.path.isfile(pid_file):
        while(1):
            with open(pid_file,"r") as fp:
                pid = fp.read()
            ret = os.system("tasklist | find \"python\" | find \" {} \"".format(pid))
            if ret != 0:break
            print("等待进程{}结束\n".format(pid))
            time.sleep(2)
    myPid = str(os.getpid())
    print(pid_file)
    with open(pid_file,"w") as fp:
        fp.write(myPid)



if __name__ == "__main__":
    only()
    print(__file__)
    for i in range(1000):
        print(1000-i)
        time.sleep(1)

