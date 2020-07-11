import os
python = "python3"

myfile = os.path.realpath(__file__)
mypath = os.path.dirname(myfile)

def call(cmd):
    logging.info(cmd)
    ret = os.system(cmd)
    if 0 == ret:return True
    return False
    
def install_yum():
    call()


def install_samba():
    call()

