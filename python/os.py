#!/usr/bin/python3

import os
with open("wocao.txt",mode="w+") as fp:
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            #print(os.path.join(root, name))
            fp.write(os.path.abspath(os.path.join(root, name))+"\n")
