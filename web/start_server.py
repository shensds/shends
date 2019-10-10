import os
import time
myfile = os.path.realpath(__file__)
mypath = os.path.dirname(myfile)

while 1:
    os.chdir(mypath)
    os.system("python server.py")