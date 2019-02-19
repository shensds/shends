# -*- coding: gb2312 -*-
import time
import telnet

class telBase():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.tn = None
        self.open()
    def open(self):
        self.close()
        try:
            self.tn = telnet.Telnet(self.host, self.port)  
            print "<telBase>:open"
        except:
            self.close()
            print "telnet %s:%s 连接失败" % (self.host, self.port)
            return True
        print "telnet %s:%s 连接成功!" % (self.host, self.port)
        return False

    def close(self):
        print "<telBase>:close"
        if self.tn != None:
            self.tn.close()
            self.tn = None
    def sendCmd(self, func, timeOut = 10, printMsg = True,):
        beginTime = time.time()
        #text = self.tn.read_very_eager()
        time.sleep(1)
        self.tn.write("%s\n" % func)
        text = self.tn.read_until("*#", 10)
        if printMsg:
            print "+++++ 时间: %s 耗时 %.3fs " % (time.strftime('%X', time.localtime(beginTime)), time.time() - beginTime)
            print "+++++ 命令: '%s' " % (func)
            print "+++++++++++++++++ 命令回显开始 ++++++++++++++++++"
            print text
            print "----------------- 命令回显结束-------------------\n"
        return  text


class telLinuxCom():
    def __init__(self, board, tool):
        self.prompt = "*"
        self.board = board
        self.tool = tool
        


if __name__ == "__main__":
    tel=telBase("10.165.86.70","10003")
    telLinuxCom("umpte", "/home/linux_x86")
    tel.sendCmd("ll")
