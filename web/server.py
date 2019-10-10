import logging
from threading import Thread
import os
import subprocess
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
import socket

myfile = os.path.realpath(__file__)
mypath = os.path.dirname(myfile)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


s = socket.socket()
ip = get_host_ip()
ip = (ip, 8001)
logging.info("绑定地址：%s"%str(ip))
s.bind(ip)
s.listen()

def prase_date(date):
    data_str = str(data, encoding="utf-8")
    l1 = data_str.split("\r\n")
    # header = l1[0]
    l2 = l1[0].split()
    url = l2[1]
    logging.info("URL：%s" % str(url))
    #以？拆分路径和参数
    index = url.find("?")
    if index != -1:
        path = url[:index]
        args = url[index+1:]
    else:
        path = url
        args = ""
    path_list = path.split("/")
    logging.info(path_list)
    #获取path绝对路径
    path = mypath
    for i in path_list:
        path = os.path.join(path,i)
    logging.debug("real path:%s"%path)

    if os.path.isfile(path):
        dir = os.path.dirname(path)
        file = os.path.basename(path)
    elif os.path.isdir(path):
        dir = path
        file = ""
    else:
        logging.error("路径 %s 不存在"%path)
        return "", "", ""
    logging.debug("dir:%s" % dir)
    logging.debug("file:%s" % file)
    logging.debug("args:%s" % args)
    return dir, file, args

def get_response(dir, file, args):
    header = b'http/1.1 200 OK\r\ncontent-type:text/html; charset=utf-8\r\n\r\n'
    if dir == "" :
        return header, b"404"
    os.chdir(dir)
    if file == "":
        file = os.path.join(mypath,"index.html")


    ef_dict = {
              ".gif"  : "image/gif",
              ".html" : "text/html; charset=utf-8",
              ".htx"  : "text/html; charset=utf-8",
              ".ico"  : "image/x-icon",
              ".jpg"  : "application/x-jpg",
    }
    header = b'http/1.1 200 OK\r\ncontent-type:application/octet-stream\r\n\r\n'
    for i in ef_dict:
        if i in file:
            header = 'http/1.1 200 OK\r\ncontent-type:' + ef_dict[i] + '\r\n\r\n'
            header = bytes(header,encoding="utf-8")
            break
    logging.info("打开文件:%s" % file)
    response = open(file,"rb").read()
    return header,response

def py(conn,dir, file, args):
    header = b'http/1.1 200 OK\r\ncontent-type:text/html; charset=utf-8\r\n\r\n'
    os.chdir(dir)
    cmd = "python %s %s"%(file,args)
    logging.info(cmd)
    cmd_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
    conn.send(header)
    while cmd_process.poll() is None:
        r = cmd_process.stdout.readline().decode()
        r = r.replace("\r\n","<br>").encode()
        conn.send(r)
    conn.close()
    return

def start(conn,data):
    print("\n\n")
    dir, file, args = prase_date(data)
    if ".py" in file:
        py(conn,dir, file, args)
        return
    header,response = get_response(dir, file, args)
    conn.send(header)
    conn.send(response)
    conn.close()

while 1:
    conn, _ = s.accept()
    data = conn.recv(8096)
    thread = Thread(target= start,args=(conn,data))
    thread.start()