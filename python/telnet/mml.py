import logging
import telnetlib
import time
import rsa
import binascii
from  threading import Thread
class TelnetClient():
    def __init__(self,host_ip,port):
        self.host_ip = host_ip
        self.port = port
        self.tn = telnetlib.Telnet(self.host_ip,port=self.port)
        self.st = 1
    def operate(self):
        self.thread1 = Thread(target = self.wocao)
        self.thread1.start()
        while 1:
            a = input("\n请输入命令\n1  :DSP BRD      2  :DSP BRDVER\n3  :查看网元     \
4  :查看主控板自检状态\ndld:下载软件包  add:添加单板\nact:激活单板\n")
            if a == '1':a = 'DSP BRD:;'
            elif a == '2':a = 'DSP BRDVER:;'
            elif a == '3':a = 'DSP SOFTSTATUS:;'
            elif a == '4':a = 'DSP SWTSTRESULT: CN=0, SRN=0, SN=6;'
            elif a == 'dld':
                b = input("\n软件包位置,输入0取消\n")
                if b == '0':continue
                a = "DLD SOFTWARE: IP=\"10.165.86.70\", USR=\"admin\", PWD=\"admin\", DIR=\"D:\sftp\software\\" + b + '\", SWT=SOFTWARE, DL=NO, ATL=GBTS&NodeB&eNodeB&gNodeB;'
            elif a == 'act':a = self.act_software()
            elif a == 'add':
                b = 1
                while b:
                    a = ""
                    b = input("\n0  ：退出\n1  ：添加5900柜\n2  ：添加5900框\n3  ：添加ubbpfw\n4  ：添加umpt\n")
                    if b == '1':cmd = "ADD CABINET: CN=0, TYPE=BTS5900;"
                    elif b == '2':cmd = "ADD SUBRACK: CN=0, SRN=0, TYPE=BBU5900;"
                    elif b == '3':cmd = "ADD BRD: SN=0, BT=UBBP-W, BBWS=GSM-0&UMTS-0&LTE_FDD-0&LTE_TDD-0&NBIOT-0&NR-0;"
                    elif b == '4':cmd = "ADD BRD: SN=6, BT=UMPT;"
                    else:pass
                    self.sendCmd(cmd,printMsg = None,re = None)
            if ';'in a:
                self.sendCmd(a,printMsg = None,re = None)

    def wocao(self):
        print("子线程开启\n")
        self.st = 1
        self.prompt = '---    END'.encode('ascii')
        while self.st:
            text = self.tn.read_until(self.prompt,timeout=10).decode('ascii')
            print(text)
        print("子线程结束\n")
    def add_brd(self):
        self.prompt = '---    END'.encode('ascii')
        ret,text=self.sendCmd("ADD CABINET: CN=0, TYPE=BTS5900;")
        ret,text=self.sendCmd("ADD SUBRACK: CN=0, SRN=0, TYPE=BBU5900;")
        ret,text=self.sendCmd("ADD BRD: SN=3, BT=UBBP, BBWS=GSM-0&UMTS-0&LTE_FDD-0&LTE_TDD-0&NBIOT-0&NR-0;")
        ret,text=self.sendCmd("ADD BRD: SN=6, BT=UMPT;")

        print("\n下载成功！！！")

    def act_software(self):
        print("等待线程1结束。。。。。。\n")
        self.st = 0
        self.thread1.join():
        time.sleep(0.5)
        self.prompt = '---    END'.encode('ascii')
        ret,text=self.sendCmd("LST SOFTWARE:;",expect="TCODE = 0  Operation succeeded.") 
        self.thread1 = Thread(target = self.wocao)
        self.thread1.start()
        if ret != True:return 0
        pkg = 0
        for line in text.split("\r\n"):
            lineList = line.split()
            if "Standby" in lineList:
                pkg = lineList[3]+ " " + lineList[4]
                break
        if pkg == 0:return 0
        print("即将激活：",pkg)
        cmd = 'ACT SOFTWARE: OT=NE, SWT=SOFTWARE, SV="%s", ATL=GBTS&NodeB&eNodeB&gNodeB;' %pkg
        xxx = input("输入1继续")
        if xxx == '1':pass
        else:cmd = None
        print(cmd)
        return cmd
    def login_mml(self):
        pwd="hwbs@com"
        self.prompt = '---    END'.encode('ascii')
        ret,text=self.sendCmd('LGI REQUEST: OP="admin", DN=0, TYPE=PUBLICKEY, HASHAL=SHA256, SID=0;',expect="RETCODE = 0  Operation succeeded")
        if ret != True:
            print(text)
            print ("MML登录step1失败!")
            return False
        else:
            print ("MML登录step1成功!")
        lines = text.splitlines(False)
        for line in lines:
            if 'Public Key  =' in line:
                pub_key = line.replace('Public Key  =', '').strip()
            elif 'Random  =' in line:
                rand = line.replace('Random  =', '').strip()
            elif 'Session ID  =' in line:
                session_id = line.replace('Session ID  =', '').strip()
        pwds = self.encrypt_str_by_rsa(pub_key, rand, pwd).decode().strip()
        mml = 'LGI: OP="admin", PWD="%s", DN=0, AUTHTYPE=PUBLICKEY, RAND="%s", SID=%s;' % ( pwds, rand, session_id)
        ret, text = self.sendCmd(mml, expect = "RETCODE = 0  Operation succeeded")
        if ret != True:
            print(text)
        else:
            print("MML登录step2成功!")
        return ret
        ret, text = self.sendCmd("neg opt:on=cc,st=off;", expect = "RETCODE = 0  Operation succeeded")
        if ret != True:
            print(text)
        else:
            print("设置不断连成功!")
        return ret
    def encrypt_str_by_rsa(self,public_key, rand, passwd):
        '''rsa encrypt string
        '''
        rand = rand.encode('ascii')
        passwd= passwd.encode('ascii')
        org_msg = binascii.a2b_hex(rand) + passwd
        pk = rsa.PublicKey._load_pkcs1_der(binascii.a2b_hex(public_key[48:]))
        enc_msg = rsa.encrypt(org_msg, pk)
        return binascii.b2a_hex(enc_msg)

    def sendCmd(self, func, timeOut = 10, expect = None, match = None, printMsg = True,re = True):
        beginTime = time.time()
        self.tn.write(func.encode('ascii') + b'\n')
        time.sleep(1)
        if re == True:
            text = self.tn.read_until(self.prompt,timeout=10)
            text = text.decode().strip()
            if printMsg:
                print ("+++++ 时间: %s 耗时 %.3fs " % (time.strftime('%X', time.localtime(beginTime)), time.time() - beginTime))
                print ("+++++ 命令: '%s' " % (func))
                print ("+++++++++++++++++ 命令回显开始 ++++++++++++++++++")
                print (text)
                print ("----------------- 命令回显结束-------------------\n")
            ret = True
            if expect != None:
                if -1 == text.find(expect):
                    ret = False
            if match != None:
                rst = re.search(expect, text)
                if rst == None: ret = False
            return ret, text


    def execute_some_command(self,command):
        command_result = self.tn.read_very_eager().decode('ascii')


if __name__ == '__main__':

    #host_ip = '100.106.252.146'
    host_ip = '100.107.253.191'
    port = "6000"
    tel = TelnetClient(host_ip,port)
    tel.login_mml()
    tel.operate()

