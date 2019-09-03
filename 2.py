# -*- coding: gb2312 -*-
import ConfigParser
import glob
import os
import logging
import time
import subprocess
import platform

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )


class BakUp():
    def __init__(self, cfg):
        self.cfg = cfg
        #���ݳɹ������Ŀ���ļ���д����ļ�
        self.backUpSuccess = 'BackUpSuccess'
        self.backUpToLocal = 'BackUpToLocalSuccss'
        self.ifwrite = False
        
    def run(self):
        # �ֶ�ָ���汾
        if self.cfg['smoke']['successver'] != '':
            successVer = os.path.join(self.cfg['smoke']['pkgdir'], self.cfg['smoke']['successver'])
            successVer = os.path.basename(successVer)
            logging.info("���ν�����ָ���汾��%s"%successVer)
        else:
            successVer = self.findLastSuccessVersion()
            if False is successVer:return False
        if not self.shareVersion(successVer):return False
        self.printInfo(successVer)
    
    def printInfo(self,successVer):
        log = 'HERT BBU ÿ�չ���������汾��ð��ͨ��\n'
        log += '�ڵ�:%s �ļ��д���ʱ�䣺%s\n'%(successVer,self.getCreateTime(successVer))
        log += '���������·����%s\n'%os.path.join(self.cfg['share']['yunxia'],successVer)
        log += '���������·��2��%s\n'%os.path.join(self.cfg['share']['yunxia2'],successVer)
        log += '����汾��%s'%self
        print(log)
        if self.ifwrite:
            fp = open(self.cfg['commit']['backupsuccess'],'w')
            fp.write(log)
            fp.close()
            
    def copyDir(self, srcDir, dst):
        cmd = r"xcopy %s %s /s /e /i /y /q /z" % (srcDir, dst)
        logging.info(cmd)
        ret, text = self.getstatusoutput(cmd)
        logging.info(text)
        if ret !=0:return False
        return True

    def getstatusoutput(self, cmd):
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

    def getCreateTime(self, successVer):
        createTime = os.path.getctime(os.path.join(self.cfg['smoke']['pkgdir'], successVer))
        createTime = time.localtime(createTime)
        createTime = time.strftime('%Y-%m-%d %X', createTime)
        return createTime


    def shareVersion(self, successVer):
        dst = os.path.join(self.cfg['share']['yunxia'],successVer)
        successFile = os.path.join(dst,self.backUpSuccess)
        if os.path.isfile(successFile):
            logging.info('%s�Ѿ�������ɣ��������豸��'%dst)
            return True
        else:
            srcDir = self.getSrcDir(successVer)
            if not self.copyDir(srcDir, dst):return False
            #���ݳɹ���д���ļ�
            open(successFile,'w').close()
            self.ifwrite = True
        # 2
        dst2 = os.path.join(self.cfg['share']['yunxia2'],successVer)
        if not self.copyDir(dst, dst2):return False
        return True
    
    def getSrcDir(self,successVer):
        srcDir = os.path.join(self.cfg['smoke']['pkgdir'], successVer)
        # ������ش������������ֱ�Ӵӱ��������¿���
        if os.path.isfile(os.path.join(self.cfg['smoke']['localpkgdir'], successVer, self.backUpToLocal)):
            logging.info("���ش��ڸð汾��ֱ�Ӵӱ��������¿���")
            # ��ok.txt����������
            os.system("xcopy %s\\*.txt %s\\ /y " % (srcDir, os.path.join(self.cfg['smoke']['localpkgdir'], successVer)))
            srcDir = os.path.join(self.cfg['smoke']['localpkgdir'], successVer)
        return srcDir
    
    def findLastSuccessVersion(self):
        fileList = glob.glob(os.path.join(self.cfg['smoke']['pkgdir'], cfg['basic']['prefix'] + '*'))
        fileList.sort(key=lambda x: os.path.getctime(x))
        fileList.reverse()
        for subDir in fileList:
            if not self.isSuccessVersion(subDir):
                continue
            subDir = os.path.basename(subDir)
            create_time = self.getCreateTime(subDir)
            logging.info("���һ��ð�̳ɹ��İ汾��%s, �ļ��д���ʱ�� %s"%(subDir,create_time))
            return subDir
        logging.error("�Ҳ���ð�̳ɹ��İ汾��")
        return None

    def isSuccessVersion(self, dirName):
        for board in self.cfg['smoke']['boardlist'].split(","):
            flgFile = "%s\\%s_ok.txt" % (dirName, board)
            if not os.path.isfile(flgFile):
                logging.info("%s is not exist!" % flgFile)
                return False
        return True


def readCfg(iniFile):
    cfg = {}
    config = ConfigParser.ConfigParser()
    config.readfp(open(iniFile))
    for section in config.sections():
        cfg[section] = {}
        for option in config.options(section):
            cfg[section][option] = config.get(section, option)
            print("cfg[%s][%s] = %s" % (section, option, config.get(section, option)))
    return cfg


if __name__ == '__main__':
    cfgFile = "hertBackUpPkg.ini"
    cfg = readCfg(cfgFile)
    bak = BakUp(cfg)
    ret = bak.run()
    if False == ret:
        logging.error("���������ʧ�ܣ�")
        exit(1)
    else:
        exit(0)
