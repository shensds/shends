import logging
import telnetlib
import time
from  threading import Thread


class TelnetClient():
    def __init__(self,host_ip,port):
        self.host_ip = host_ip
        self.port = port
        self.prompt = '$'.encode()
        try:
            self.tn = telnetlib.Telnet(self.host_ip,port=self.port)
        except:
            print(self.host_ip+":"+self.port+"连接失败")
        text = self.tn.read_until("Welcome to IPOP share server".encode(),timeout=10)
        print(self.host_ip+":"+self.port+"连接成功")
    def operate(self):
        
        self.sendCmd("echo 1")
        self.sendCmd("echo 2")
        self.sendCmd("echo 3")
        self.sendCmd("echo 4")
        self.sendCmd("echo 5")
        
    def sendCmd(self, func, timeOut = 10, expect = None, match = None, printMsg = True,re = True):
        beginTime = time.time()
        self.tn.write(func.encode('ascii') + b'\n')
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

    host_ip = '192.168.99.248'
    port = "1000"

    tel = TelnetClient(host_ip,port)
    tel.operate()



