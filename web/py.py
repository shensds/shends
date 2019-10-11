#conding:utf-8
import socket
import subprocess
import logging
import os
import sys
import importlib
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
myfile = os.path.realpath(__file__)
mypath = os.path.dirname(myfile)

def py(conn,dir, file, args):
    os.chdir(dir)
    arg_dict = {"conn":conn}
    #参数转换成字典
    if "=" in args:
        args_list = args.split("&")
        for arg in args_list:
            _ = arg.split("=")
            key = _[0]
            value = _[1]
            value = value.replace("%2F","/").replace("%5C","\\").replace("+"," ")
            arg_dict[key] = value
    print(arg_dict)
    try:
        _py = open(file,"r",encoding= "utf-8").read()
        exec(_py,arg_dict)
        conn.close()
    except Exception as e:
        e = str(e)
        print(e)
        header = b'http/1.1 200 OK\r\ncontent-type:text/html; charset=utf-8\r\n\r\n'
        conn.send(header)
        conn.send(bytes(e,encoding = "utf-8"))
        conn.close()
    return
    

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
    
    
def prase_date(data):
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
    
