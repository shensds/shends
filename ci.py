# -*- coding: gb2312 -*-

import os, sys
import glob
import shutil
import time
import logging
import subprocess
logging.basicConfig(level = logging.INFO,format = '%(asctime)s %(filename)s:line:%(lineno)d:%(name)s:%(levelname)s:%(message)s')

curfile = os.path.realpath(__file__)
curpath = os.path.dirname(curfile)
os.environ["WORK_SCRIPT_PATH"] = curpath
os.environ["SUCC_ROOT_PATH"] = os.path.join(os.environ["WORK_SCRIPT_PATH"], "succFiles")

SRC_PKG_DIR=r"D:\py\pkg\SRC_PKG_DIR"
SRC_PKG_DIR_TRIGGER=r"\\10.156.17.188\ctu_ci_nas\HERT_BBU\510C00_Software_Package_01"
DST_PKG_DIR=r"D:\py\pkg\DST_PKG_DIR"

PREFIX = '510C00_TRUNK_'
env_info = {
            "MBTS" : {"pkg_prefix": r"MBTS",
                      "pkg_pstfix": r"",
                      "smokeLst": ['umpt', 'umptb', 'umpte','wmpt','gtmuc','lmpt']
                     },
            "USU"  : {"pkg_prefix": r"USU",
                      "pkg_pstfix": r"",
                      "smokeLst": ['usu']
                     },
            "USU3910" : {"pkg_prefix": r"USU3910",
                      "pkg_pstfix": r"",
                      "smokeLst": ['usu3910']
                     },
            # "USE"  : {"pkg_prefix": r"USE",
                       # "pkg_pstfix": r"",
                       # "smokeLst": [r"umptb_use", "umpte_use"]
                     # },
            "GBTS"  : {"pkg_prefix": r"gbts",
                      "pkg_pstfix": r"",
                      "smokeLst": ['gbts']
                     },
        }

returnValuelst = []


'''
1����ʱ�������������Ŀ¼��������ˣ�
2����ģ�������ҵ�ð�̶�OK�Ľڵ�
3����ģ��ڵ�����һ�γɹ��ڵ�Ƚϣ���һ���Ϳ��������򲻿���
'''


def getstatusoutput(cmd):
    pipe = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    text,err = pipe.communicate()
    return pipe.returncode,text

def systemCall(cmdLine):
    ret, text = getstatusoutput(cmdLine)
    return ret, text

def getCurTimeStr():
    return time.strftime('%Y-%m-%d %X',time.localtime(time.time()))

def fileListSortByCreateTime(pkgRoot, prefix):
    '''
    ��ʱ�������������Ŀ¼��������ˣ�
    '''
    fileList = glob.glob(os.path.join(pkgRoot, prefix + '*'))
    fileList.sort(key = lambda x: os.path.getctime(x))
    fileList.reverse()
    return fileList

def isSuccVer(dirName, smokeList):
    for board in smokeList:
        flgFile = os.path.join(dirName, board + '_ok.txt')
        if not os.path.isfile(flgFile):
            return False
    return True
def findLastSuccByMod(pkgList, smokeList):
    '''
    ��ģ��Ѱ������ð��OK�������
    '''
    for pkgDir in pkgList:
        if isSuccVer(pkgDir, smokeList):
            return pkgDir
    return None

def copyDir(srcDir, desDir):
    # cmd = r"robocopy %s %s /E /Z /FFT /W:10 /R:5 /COPY:DT /MT:120 /ZB /NS /NC /NFL /NDL /NP /XX" %(srcDir, desDir)
    cmd = r"xcopy %s %s /y /r /i /e /s /Q" %(srcDir, desDir)
    logging.info(cmd)
    ret, text = systemCall(cmd)
    if ret!=0:
        print(text)
        raise AssertionError, "xcopy error!!!"
    return True
    
def clearDir(dire):
    if os.path.isdir(dire):
        cmd = "rmdir /s/q \"%s\"" %(dire)
        logging.info(cmd)
        getstatusoutput(cmd)

def copyPkg(srcPkg, desModDir, pkg_prefix, pkg_pstfix):
    try:
        # ���ģ�������
        clearDir(desModDir)
        # ����������
        srcCommDir = os.path.join(srcPkg, pkg_prefix)
        desCommDir = os.path.join(desModDir, pkg_pstfix)
        copyDir(srcCommDir, desCommDir)
        pkg_prefix = pkg_prefix.split('\\')[0]
        # �����䲹��
        for srcSpcDir in glob.glob(os.path.join(srcPkg, 'SPC', pkg_prefix + '*')):
            logging.info(srcSpcDir)
            desSpcDir = os.path.join(desModDir, 'SPC', os.path.basename(srcSpcDir))
            copyDir(srcSpcDir, desSpcDir)

        if pkg_prefix == "TDS": patType = "*_T"
        else:   patType = pkg_prefix + '_*'
        # �����Ȳ���
        for srcSphDir in glob.glob(os.path.join(srcPkg, 'Hotpatch', patType)):
            desSphDir = os.path.join(desModDir, 'HotPath', os.path.basename(srcSphDir))
            copyDir(srcSphDir, desSphDir)
    except:
        print("%s :���������쳣"%mod)
        print sys.exc_info()[0],sys.exc_info()[1]
        returnValuelst.append([mod, False])


def mkDir(fileName):
    fileName = os.path.abspath(fileName)
    dirList = fileName.split(os.sep)
    dirName = dirList[0]
    if dirName == "":
        beginIdx = 3
    else:
        beginIdx = 1
    for i in range(1, len(dirList)):
        dirName += os.sep + dirList[i]
        if i <= beginIdx: continue
        if not os.path.isdir(dirName):
            os.mkdir(dirName)

def writeSucc(succfile, ver):
    fp = open(succfile, 'w')
    fp.write(ver)
    fp.close()

def readLine(file):
    fp = open(file)
    text = fp.read()
    text = text.split()[0]
    text = text.strip()
    fp.close()
    return text

def readLastSucc(succFile):
    if os.path.isfile(succFile):
        return readLine(succFile)
    return None

def copyRes(srcPkg, desModDir, pkgList):
    resDir = os.path.join(srcPkg, "artifacts", "res")
    if os.path.isdir(resDir):
        cmd = "xcopy %s\\*macro_en.ini %s\\res\\ /y/r/i/s" %(resDir, desModDir)
        logging.info(cmd)
        getstatusoutput(cmd)
    return True


def singleModCpSoftware(pkgList, mod):
    logging.info("��ʼ����ģ��{}".format(mod))
    logging.info("ð���б�{}".format(env_info[mod]['smokeLst']))
    succPkg = findLastSuccByMod(pkgList, env_info[mod]['smokeLst'])
    if not succPkg:
        logging.error("ģ��%s�޿��ð�\r\n" %mod)
        return True
    logging.info("�ҵ�ģ��{}���ð汾{}".format(mod,succPkg))
    succFile = os.path.join(os.environ["SUCC_ROOT_PATH"], mod, "succ.txt")
    succVersion = os.path.basename(succPkg)
    if succVersion == readLastSucc(succFile):
        logging.info("ģ��%s�İ汾δ����\r\n" %mod)
        return True

    logging.info("����ģ��%s:\n" %mod)
    desModDir = os.path.join(DST_PKG_DIR, mod)   # �Զ������Ը�ģ��ĸ�Ŀ¼����HERT306C00_Daily_Soft\LTE
    copyPkg(succPkg, desModDir, env_info[mod]['pkg_prefix'], env_info[mod]['pkg_pstfix'])
    copyRes(succPkg, desModDir, pkgList)
    mkDir(os.path.dirname(succFile))
    writeSucc(succFile, succVersion)
    writeSucc(os.path.join(desModDir, "succ.txt"), succVersion)

def updateAutociPkg(pkgRoot, prefix, env_info, desPkgDir):
    pkgList = fileListSortByCreateTime(pkgRoot, prefix)
    for i in pkgList:
        print(i)

    #��������250ʱִ������
    while(len(pkgList) > 250):
        logging.info("��ʼ����{}".format(pkgList[-1]))
        cmd = "rmdir /s /q %s" %(pkgList[-1])
        logging.info(cmd)
        ret = os.system(cmd)
        if ret !=0: logging.error("rm old dir fail")
        pkgList = fileListSortByCreateTime(pkgRoot, prefix)
    for mod in env_info.keys():
        singleModCpSoftware(pkgList, mod)
        # t = threading.Thread(target=singleModCpSoftware, args=(pkgList, mod, ))
    return True

if __name__ == "__main__":
    updateAutociPkg(SRC_PKG_DIR, PREFIX, env_info, DST_PKG_DIR)
    print '*' * 50
    print "\nupdate finished!\n"
    print '*' * 50
    for ret in returnValuelst:
        if ret[1] == False:
            print("ģ��[%s]���Զ���copy�����ʧ�ܣ����ע"%ret[0])
            exit(1)
    cmd = r"xcopy %s %s /y/r/i/e/s" %(os.environ["SUCC_ROOT_PATH"], os.path.join(SRC_PKG_DIR_TRIGGER, "trigger", "AutoSuccFiles"))
    logging.info(cmd)
    ret, text = systemCall(cmd)
    exit(0)
