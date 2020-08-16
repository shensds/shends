# coding=utf-8
"""
Python FTP 操作
from ftplib import FTP      # 加载ftp模块
ftp = FTP()                 # 获取FTP对象
ftp.set_debuglevel(2)       # 打开调试级别2，显示详细信息
ftp.connect('IP', PORT) # 连接ftp，server和端口
ftp.login('user', 'password')  # 登录用户
print(ftp.getwelcome())     # 打印欢迎信息
ftp.cmd('xxx/xxx')          # 进入远程目录
bufsize = 1024              # 设置缓存区大小
filename='filename.txt'     # 需要下载的文件
file_handle=open(filename, 'wb').write   # 以写的模式在本地打开文件
file.retrbinaly('RETR filename.txt', file_handle,bufsize)  # 接收服务器上文件并写入本地文件
ftp.set_debuglevel(0)       # 关闭调试模式
ftp.quit                    # 退出ftp
ftp相关的命令操作
ftp.cwd(pathname)           # 设置FTP当前操作的路径
ftp.dir()                   # 显示目录下所有目录的信息
ftp.nlst()                  # 获取目录下的文件
ftp.mkd(pathname)           # 新建远程目录
ftp.rmd(dirname)            # 删除远程目录
ftp.pwd()                   # 返回当前所在位置
ftp.delete(filename)        # 删除远程文件
ftp.rename(fromname, toname)    #将fromname改为toname
ftp.storbinaly('STOR filename.txt',file_handel,bufsize)  # 上传目标文件
ftp.retrbinary('RETR filename.txt',file_handel,bufsize)  # 下载FTP文件
"""
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
import os
from ftplib import FTP

class FtpClicent():
    def __init__(self):
        self.ftp = FTP()
        host = "192.168.123.185"
        port = 2121
        user = ""
        passwd = ""
        self.login(host, port, user, passwd)
        logging.info("登录成功")
        #远程目录列表
        self.exists = set()

    def login(self, host, port, user, passwd):
        logging.info("开始连接...")
        self.ftp.connect(host, port)
        logging.info("连接成功")
        self.ftp.login(user, passwd)
        logging.info("登录成功")
        self.ftp.encoding = 'utf-8'

    def listdir(self,path):
        _list = self.ftp.nlst(path)
        list = []
        for i in _list:
            list.append(i.lower())
        return list

    def mkdir(self,path):
        if path in self.exists:
            #logging.info("路径%s存在"%path)
            return
        if path == "":
            return
        self.exists.add(path)
        logging.info(path)
        path_list = path.split("/")
        path = ""
        for i in path_list:
            x = self.listdir(path)
            if path == "":
                path = i
            else:
                path += "/" + i
            if i.lower() not in x:
                 logging.info(path)
                 self.ftp.mkd(path)

    def ls_l(self, *args):
        cmd = 'LIST'
        for arg in args:
            cmd = cmd + (' ' + arg)
        files = []
        self.ftp.retrlines(cmd, files.append)
        return files
        
    def get_dir_file(self,path,list):
        path_list = self.ls_l(path)
        dir_list = []
        file_list = []
        for i in path_list:
            name = i[51:]
            name = path + "/" + name
            if i[0] == "d":
                dir_list.append(name)
            else:
                file_list.append(name)
        list += file_list
        for i in dir_list:
            self.get_dir_file(i,list)
                
    def get_file_list(self,path):
        list = []
        self.get_dir_file(path,list)
        return list

    def downloadfile(self, remotepath, localpath=None):
        """ 下载文件 """
        bufsize = 1024
        if localpath is None:
            localpath = os.path.basename(remotepath)
        fp = open(localpath, 'wb')
        self.ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
        fp.close()
        print(f'文件 {remotepath} 下载成功！')

    def uploadfile(self, localpath, remotepath=None):
        """ 上传文件 """
        bufsize = 1024
        if remotepath is None:
            remotepath = os.path.basename(localpath)
        fp = open(localpath, 'rb')
        #目录不存在时先新建
        dir = os.path.dirname(remotepath)
        self.mkdir(dir)
        self.ftp.storbinary('STOR ' + remotepath, fp, bufsize)
        fp.close()
        print(f'文件 {localpath} 上传成功！')


def to_windows():
    ftp = FtpClicent()
    list = ftp.get_file_list("music")
    print(list)
    dst = "e:\\music"
    for i in list:
        dst_file = os.path.join(dst,i.replace("/","\\"))
        if not os.path.isdir(os.path.dirname(dst_file)):
            cmd = "mkdir %s"%os.path.dirname(dst_file)
            print(cmd)
            os.system(cmd)
        if not os.path.exists(dst_file) or os.path.getsize(dst_file) < 3172:
            ftp.downloadfile(i,dst_file)


dst = "e:\\music\\"
def to_phone():
    ftp = FtpClicent()
    list = []
    for root, dirs, files in os.walk(dst, topdown=False):
        for name in files:
            list.append(os.path.join(root, name))
    phone_list = ftp.get_file_list("music")
    for i in list:
        dst_file = i.replace(dst,"")
        dst_file = dst_file.replace("\\","/")
        #print(dst_file)
        if dst_file in phone_list:
            continue
        print(i)
        ftp.uploadfile(i,dst_file)

def test():
    ftp = FtpClicent()
    ftp.mkdir("music/华语/1/2/3")
    ftp.mkdir("music/华语/1/2/3")
    #ftp.uploadfile(r"e:\music\music\华语\1983组合 - 等爱走了以后.mp3","music/华语/1983组合 - 等爱走了以后.mp3")
#ftp.downloadfile("1.file","d:\\1.file")
#to_phone()
to_windows()




