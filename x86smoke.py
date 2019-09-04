# -*- coding: gb2312 -*-
import sys
import glob
import os
import logging
import time
import ConfigParser

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )

class x86smoke():
    def __init__(self,argv):
        #ftp目录
        self.ftp_path = r'D:\tmp\dst'
        #保留旧软件包的数量
        self.max_pkg_num = 5
        #冒烟脚本路径
        self.testCase = r"D:\tmp"
        #功能
        self.function = self.getFunction(argv[1])
        self.artifacts = argv[2]
        self.git_no = argv[3]
        self.src = os.path.join(self.artifacts,"tmp","src")
        self.dst = os.path.join(self.ftp_path, "pkg_" + self.git_no)
        
    def getFunction(self,func):
        if func == "copy":
            return self.copyPkg
        else:
            self.brd = func
            return self.runCase
            
    def run(self):
        return self.function()

    def runCase(self):
        #修改配置文件
        self.changePkgDir()
        os.chdir(self.testCase)
        cmd = "python -u %s.py"%self.brd
        logging.info(cmd)
        ret = os.system(cmd)
        if ret !=0:
            return False
        return True

    def changePkgDir(self):
        ini_file = os.path.join(self.testCase,self.brd + '.ini')
        logging.info("开始修改%s文件"%ini_file)
        config = ConfigParser.ConfigParser()
        config.read(ini_file)
        config.set("ftp", "dir", self.dst)
        config.write(open(ini_file, "r+")) 
        
    def copyPkg(self):
        #删除旧版本软件包
        self.rmPkg()
        #拷贝软件包
        ret = self.copyDir()
        return ret
        
    def copyDir(self):
        logging.info("pkg_src:%s"%self.src)
        logging.info("pkg_dst:%s"%self.dst)
        cmd = r"xcopy %s %s /s /e /i /y /q /r" % (self.src,self.dst)
        logging.info(cmd)
        ret = os.system(cmd)
        if ret !=0:return False
        return True

    def rmPkg(self):
        flag = True
        fileList = glob.glob(os.path.join(self.ftp_path,'pkg_*'))
        if len(fileList) <= self.max_pkg_num:
            logging.info("当前软件包数量：%s，无需清理..."%len(fileList))
            return True
        logging.info("当前软件包数量：%s"%len(fileList))
        fileList.sort(key=lambda x: os.path.getctime(x))
        rm_num = len(fileList) - self.max_pkg_num
        for subDir in fileList:
            if rm_num <=0:
                return flag
            rm_num -= 1
            pkg_dir = os.path.join(self.ftp_path,subDir)
            logging.info("开始清理%s，文件夹创建时间：%s"%(pkg_dir,self.getCreateTime(pkg_dir)))
            cmd = "rd /s /q %s"%pkg_dir
            logging.info(cmd)
            ret = os.system(cmd)
            if ret != 0:
                logging.error("软件包%s删除失败"%pkg_dir)
                flag = False
        return flag
        
    def getCreateTime(self,dir):
        createTime = os.path.getctime(dir)
        createTime = time.localtime(createTime)
        createTime = time.strftime('%Y-%m-%d %X', createTime)
        return createTime


if __name__ == '__main__': 

    print(sys.argv)
    smoke = x86smoke(sys.argv)
    ret = smoke.run()
    if False == ret:
        exit(1)
    else:
        exit(0)
    

