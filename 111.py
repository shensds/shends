import logging
import os
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
myfile = os.path.realpath(__file__)
mypath = os.path.dirname(myfile)

import subprocess
def getstatusoutput(cmd):
    """
    Purpose:
    Globals:
    Arguments:
    Returns:
    """





getstatusoutput("python 1.py")