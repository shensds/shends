import os,sys

smb_conf = '''
[global]
        #用户组
        workgroup = WORKGROUP
        security = user
        map to guest = Bad User
        passdb backend = tdbsam
        printing = cups
        printcap name = cups
        load printers = yes
        cups options = raw
        ntlm auth = yes

[homes]
        comment = Home Directories
        valid users = %S, %D%w%S
        browseable = No
        read only = No
        inherit acls = Yes
        
[gen]
        comment = share folder
        browseable = yes
        path = /
        valid users = @root
        write list = @roots
        #force user = root
        #force group = root
        create mask = 0777
        directory mask = 0777
        public = no 
        available = yes 
        writable = yes
        printable = no
'''

import subprocess
import platform
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )

class logger():
    def __init__(self):
        pass
    def write(str):
        print(str)
    def flush():
        pass

def getstatusoutput(cmd):
    """
    Purpose:
    Globals:
    Arguments:
    Returns:
    """
    cmd_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cmd_echo = cmd_process.stdout.read()
    cmd_process.stdout.close()
    sts = cmd_process.wait()
    try:
        cmd_echo = cmd_echo.decode('UTF-8')
    except UnicodeDecodeError:
        cmd_echo = cmd_echo.decode('gbk', errors='ignore')
    if int(platform.python_version().split('.')[0]) < 3:
        if platform.system() == 'Windows':
            cmd_echo = cmd_echo.encode('gbk', errors='ignore')
        else:
            cmd_echo = cmd_echo.encode('UTF-8', errors='ignore')
    if cmd_echo[-1:] == '\n': cmd_echo = cmd_echo[:-1]
    return sts, cmd_echo

def call(cmd):
    logging.info(cmd)
    ret,text = getstatusoutput(cmd)
    if 0!=ret:return False
    return True

def install_smb():
    "apt-get install samba samba-common"
def write_conf():
    conf = "/etc/samba/smb.conf"
    if not os.path.isfile(f"{conf}.init"):
        call(f"cp {conf} {conf}.init")
    with open(conf,"w") as fp:
        fp.write(smb_conf)
        

def stop_firewalld():
    call("systemctl stop firewalld.service")
    call("systemctl disable firewalld.service")
    call("setenforce 0")

def start_smb():
    call("systemctl start smb")
    call("systemctl restart smb")
    call("systemctl enable smb")

def change_pass():
    import pexpect
    child = pexpect.spawn('smbpasswd -a root')
    child.logfile = logger
    child.expect(':')
    child.sendline('123')
    child.expect(':')
    child.sendline('123')
    
write_conf()
stop_firewalld()
change_pass()
start_smb()

'''
sudo apt-get install cifs-utils

cat /etc/issue查看当前正在运行的 Ubuntu 的版本号。

sudo apt-get upgrade
sudo apt-get update
sudo apt-get dist-upgrade



smbpasswd -a root

vim /etc/samba/smb.conf

service smbd restart


#检测配置文件是够OK
testparm
出现Loaded services file OK


groupadd co3
useradd ted -g co3 -s /sbin/nologin
smbpasswd -a ted



chown nobody:nobody /home
chown ted:co3 /home






开放端口
firewall-cmd --permanent --add-port=139/tcp
firewall-cmd --permanent --add-port=445/tcp
systemctl restart firewalld


或者直接把防火墙关了也行。

systemctl stop firewalld.service
禁止firewall开机启动
systemctl disable firewalld.service 
#SELINUX
运行命令 getenforce 获取当前selinux状态
Enforcing为开启

setenforce 0
'''