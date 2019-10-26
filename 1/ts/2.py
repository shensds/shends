import os
src = "E:\mp4"
dst = r"C:\mp4"
def get_tslist(dir):
    file_list = os.listdir(dir)
    ts_list = [] 
    for i in file_list:
        if i.endswith(".ts"):
            ts_list.append(i)
    ts_list.sort(key = lambda x:int(x.split(".")[0]))
    return ts_list
    
def hebing(dir):
    ts_dir = os.path.join(src,dir)
    ts_list = get_tslist(ts_dir)
    mpsfile = os.path.join(dst,dir + ".mp4")
    fp = open(mpsfile,"wb")
    for i in ts_list:
        tsfile = os.path.join(ts_dir,i)
        print(tsfile)
        with open(tsfile,"rb") as ts_fp:
            _ts = ts_fp.read()
            fp.write(_ts)

dir_list = os.listdir(src)
for i in dir_list:
    hebing(i)