import logging
import telnetlib
import time
from  threading import Thread
class TelnetClient():
    def __init__(self,host_ip,port):
        self.host_ip = host_ip
        self.port = port
        self.tn = telnetlib.Telnet(self.host_ip,port=self.port)
        self.st = 1
        self.prompt = '$'.encode()
    def operate(self):
        #self.thread1 = Thread(target = self.wocao)
        #self.thread1.start()
        a = "pwd"
        #self.tn.write(xxx)
        #self.tn.write(xxx)
        self.sendCmd(a)
        time.sleep(1)
        self.tn.write(b"\n")
        time.sleep(1)
        self.tn.write(b"\n")
        time.sleep(1)
        self.tn.write(b"\n")
        time.sleep(1)
        self.tn.write(b"\n")
        time.sleep(1)
        self.tn.write(b"\n")
        time.sleep(1)
        self.tn.write(b"pwd\n")
        time.sleep(1)
        self.tn.write(b"\n")
        time.sleep(1)
        self.sendCmd(a)


        print("-------------")



    def sendCmd(self, func, timeOut = 10, expect = None, match = None, printMsg = True,re = True):
        beginTime = time.time()
        xxx = func.encode('ascii') + b'\n'
        time.sleep(1)
        self.tn.write(xxx)
        print(xxx)
        if re == True:
            time.sleep(1)
            text = self.tn.read_until(b"root",timeout=10)
            print("xxxxxxxxxxxxx")




    def execute_some_command(self,command):
        command_result = self.tn.read_very_eager().decode('ascii')


if __name__ == '__main__':

    host_ip = '127.0.0.1'
    port = "1000"
    tel = TelnetClient(host_ip,port)
    tel.operate()

