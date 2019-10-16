import logging
from threading import Thread
import os
import socket
import importlib
from urllib.parse import unquote
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
myfile = os.path.realpath(__file__)
mypath = os.path.dirname(myfile)

g_html = '''http/1.1 200 OK\r\ncontent-type:text/html; charset=utf-8\r\n\r\n
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for {dir}</title>
</head>
<body>
<h1>Directory listing for {dir}</h1>
<hr>
<ul>
{li}
</ul>
<hr>
<ul>
{zip}
</ul>
<hr>
</body>
</html>
'''
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
ip = "0.0.0.0"
ip = (ip, 8001)
logging.info("绑定地址：%s"%str(ip))
s.bind(ip)
s.listen()

def prase_date(data):
    data_str = str(data, encoding="utf-8")
    l1 = data_str.split("\r\n")
    # header = l1[0]
    l2 = l1[0].split()
    url = l2[1]
    logging.info("URL：%s" % str(url))
    url = unquote(url, 'utf-8')
    logging.info("URL_____：%s" % str(url))
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
    
def get_html(dir, file, args):
    dir_listdir = os.listdir(dir)
    dirs = ""
    files = ""
    this_dir = dir.replace(mypath,"")
    zip = "<li><a href=\"%s?zip\">%s</a></li>\n"%(this_dir,"打包下载")
    b_dir = os.path.realpath(os.path.join(dir,".."))
    b_dir = b_dir.replace(mypath,"")
    li =  "<li><a href=\"%s/\">%s</a></li>\n"%(b_dir,"返回上层目录")

    for i in dir_listdir:
        logging.debug(os.path.join(dir,i))
        if os.path.isfile(os.path.join(dir,i)):
            files += "<li><a href=\"%s\">%s</a></li>\n"%(i,i)
        else:
            dirs += "<li><a href=\"%s/\">%s/</a></li>\n"%(i,i)
    li += dirs
    li += files
    html = g_html.replace("{dir}",dir)
    html = html.replace("{li}",li)
    html = html.replace("{zip}", zip)
    return html

def dld_file(conn,dir, file, args):
    header = b'http/1.1 200 OK\r\ncontent-type:application/octet-stream\r\n\r\n'
    conn.send(header)
    os.chdir(dir)
    logging.info("打开文件:%s" % file)
    response = open(file,"rb").read()
    conn.send(response)
    conn.close()

def zip_file(conn, dir):
    import zipfile
    header = b'http/1.1 200 OK\r\ncontent-type:application/octet-stream\r\n\r\n'
    conn.send(header)
    os.chdir(dir)
    logging.info("打开文件:%s" % file)
    response = open(file,"rb").read()
    conn.send(response)
    conn.close()

def start(conn,data):
    print("\n\n")
    dir, file, args = prase_date(data)
    if args == "zip":
        return zip_file(conn, dir)
    if dir == "":
        conn.close()
        return
    if file == "":
        _html = get_html(dir, file, args)
        _html = bytes(_html, encoding="utf-8")
        conn.send(_html)
        conn.close()
        return

    return dld_file(conn,dir, file, args)


while 1:
    conn, _ = s.accept()
    data = conn.recv(8096)
    thread = Thread(target= start,args=(conn,data))
    thread.start()
