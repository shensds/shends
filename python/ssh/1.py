import os,sys
import subprocess
import platform
import logging
try:
    import pexpect
except:
    os.system("python -m pip install pexpect")
    import pexpect
myfile = os.path.realpath(__file__)
mypath = os.path.dirname(myfile)
logfile = os.path.join(mypath, "ssh.txt")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
'''
process = pexpect.spawn("/bin/bash", ["-c", cmd])
process.expect(pexpect.EOF)
sendline("ls –l", cwd="/etc") 
process.expect(pattern_list, timeout=-1, searchwindowsize=None)  searchwindowsize 匹配数量
process.sendcontrol('g') ctrl_g
sendeof() - 向子程序发送 End Of File 信号。
sendintr() - 发送终止信号
process.close(force=True)
isalive() - 检查子程序运行状态
'''
class Linux():
    def __init__(self, ip, port,usr, pwd):
        self.ip = ip
        self.port = port
        self.usr = usr
        self.pwaawd = pwd
        self.process = None
        
    def _print(self, child):
        print("%s%s" % (child.before.decode(errors='ignore'), child.after.decode(errors='ignore')))
        
    def login(self):
        ssh_newkey = 'Are you sure you want to continue connecting'
        child = pexpect.spawn('ssh %s@%s -p %s' % (self.usr, self.ip, self.port))
        log = open(logfile,"ab+")
        child.logfile = log
        i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
        if i == 0: # Timeout
            logging.error("%s login fail" % self.ip)
            logging.info("%s\n%s" % (child.before, child.after))
            return False

        if i == 1: # SSH does not have the public key. Just accept it.
            child.sendline ('yes')
            i = child.expect([pexpect.TIMEOUT, 'password: '])
            if i == 0: # Timeout
                logging.error("%s login fail" % self.ip)
                logging.info("%s%s" % (child.before, child.after))
                return False
        child.sendline(self.pwaawd)
        self.process = child
        
    def __del__(self):
        if None != self.process:
            self.process.close(force=True)
        
        
a = Linux("192.168.123.135", 22,"root","123")
a.login()







