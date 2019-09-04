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

def printInfo(argv):
    info = "python "
    for i in argv:
        info = "%s %s"%(info,i)
    logging.info(info)

def getCreateTime(dir):
    createTime = os.path.getctime(dir)
    createTime = time.localtime(createTime)
    createTime = time.strftime('%Y-%m-%d %X', createTime)
    return createTime

def rmPkg(ftp_path,max_pkg_num):
    flag = True
    fileList = glob.glob(os.path.join(ftp_path,'pkg_*'))
    if len(fileList) <= max_pkg_num:
        logging.info("当前软件包数量：%s，无需清理..."%len(fileList))
        return True
    logging.info("当前软件包数量：%s"%len(fileList))
    fileList.sort(key=lambda x: os.path.getctime(x))
    rm_num = len(fileList) - max_pkg_num
    for subDir in fileList:
        if rm_num <=0:
            return flag
        rm_num -= 1
        pkg_dir = os.path.join(ftp_path,subDir)
        logging.info("开始清理%s，文件夹创建时间：%s"%(pkg_dir,getCreateTime(pkg_dir)))
        cmd = "rd /s /q %s"%pkg_dir
        logging.info(cmd)
        ret = os.system(cmd)
        if ret != 0:
            logging.error("软件包%s删除失败"%pkg_dir)
            flag = False
    return flag
    
def copyDir(src, dst):
    cmd = r"xcopy %s %s /s /e /i /y /q /r" % (src,dst)
    logging.info(cmd)
    ret = os.system(cmd)
    if ret !=0:return False
    return True

def changePkgDir(testCase,smoke_list,dst):
    for ini in smoke_list:
        ini_file = os.path.join(testCase,ini)
        logging.info("开始修改%s文件"%ini_file)
        config = ConfigParser.ConfigParser()
        config.read(ini_file)
        config.set("ftp", "dir", dst)
        config.write(open(ini_file, "r+")) 


if __name__ == '__main__': 
    argv = sys.argv
    printInfo(argv)
    #ftp目录
    ftp_path = r'D:\tmp\dst'
    #保留旧软件包的数量
    max_pkg_num = 5
    #冒烟脚本路径
    testCase = r"D:\tmp"
    #冒烟列表
    smoke_list = ["umptx.ini","ubbpfw_x86.ini","umptg_x86.ini"]
    #删除旧版本软件包
    rmPkg(ftp_path,max_pkg_num)

    artifacts = argv[1]
    git_no = argv[2]
    src = os.path.join(artifacts,"tmp","src")
    dst = os.path.join(ftp_path, "pkg_" + git_no)
    logging.info("pkg_src:%s"%src)
    logging.info("pkg_dst:%s"%dst)
    #拷贝软件包
    ret = copyDir(src,dst)
    if False == ret:
        logging.error("软件包拷贝失败！")
        exit(1)
    else:
        #修改软件包路径
        changePkgDir(testCase,smoke_list,dst)
        exit(0)
