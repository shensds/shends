import os

    
def get_mu():
    src = r"E:\UC"
    file_list = os.listdir(src)
    for dir_name in file_list:
        dir = os.path.join(src,dir_name)

        if os.path.isdir(dir):
            m3u8_file_list = os.listdir(dir)
            for m3u8_file_name in m3u8_file_list:
                m3u8_file = os.path.join(dir,m3u8_file_name)
                if m3u8_file.endswith(".m3u8"):
                    m3u8_des_file = dir + ".m3u8"
                    cmd = "move \"%s\" \"%s\""%(os.path.join(src,dir,m3u8_file),os.path.join(src,m3u8_des_file))
                    os.system(cmd)
                    print(cmd)
            

    
def get_m3u8_list(m3u8):
    ts_list = []
    with open(m3u8,"r",encoding="utf-8") as fp:
        m3u8 = fp.readlines()
    for i in m3u8:
        text = r"/storage/emulated/0/UCDownloads/VideoData//"
        #text = r"file:///storage/emulated/0/QQBrowser/视频/"
        if text in i:
            i = i.replace(text,"").strip()
            #dir,file = i.split("/")
            #ts_list.append([dir,file])
            ts_list.append(i)
    print("文件列表获取成功")
    return ts_list

def start():
    src = "E:\\uc"
    dst = "E:\\h\\uc2"
    
    dir_list = os.listdir(src)
    for i in dir_list:
        print("iiii%s"%i)
        if os.path.isfile("c:\\ok\\%s"%i):
            print("???")
            continue
        if i.endswith(".m3u8"):
            print(i)
            name = i.replace(".m3u8",".mp4")
            print("开始获取文件列表")
            ts_list = get_m3u8_list(os.path.join(src,i))
            print("文件列表获取成功")
            mps4file = os.path.join(dst,name)
            print("准备写入文件%s"%mps4file)
            fp = open(mps4file,"wb")
            print("%s打开成功"%mps4file)
            for ts in ts_list:
                tsfile = os.path.join(src,ts)
                print(tsfile)
                try:
                    with open(tsfile,"rb") as ts_fp:
                        _ts = ts_fp.read()
                        fp.write(_ts)
                        print("write ok")
                except:
                    print("!!!!!!!!!!!!!!!!!!!!")
                    pass
            fp.close()
            os.system("echo xx > c:\\ok\\%s"%i)

    
    
start()
#get_mu()
    
    
    
    
    