# -*- coding: utf-8 -*-
#auther : shendongsheng

def read_cfg(inifile):
    cfg = {}
    file_list = []
    with open(inifile, "r", encoding="utf-8") as fp:
        for i in fp.readlines():
            #去除BOM
            #i = i.replace(codecs.BOM_UTF8, '')
            i = i.strip("\n").strip(" ")#.replace(" ","")
            if len(i)==0:continue
            if (i[0] =="#") or (i[0] ==";"):continue
            file_list.append(i)
    key = "comm"
    for i in file_list:
        if (i[0] == "[") and (i[-1] == "]"):
            key = i[1:-1]
            cfg[key]={}
            continue
        if "=" in i:val = i.split("=",1)
        #if ":" in i:val = i.split(":",1)
        cfg[key][val[0].strip()] = val[1].strip()
    return cfg

def write_cfg(inifile, key1, key2, val):
    flag = 0
    with open(inifile, "r", encoding="utf-8") as fp:
        cfg = fp.readlines()

    for i in range(len(cfg)):
        line = cfg[i].strip("\n").strip()
        #注释行直接跳过
        if (len(line) < 2): continue
        if line[0] in ";#": continue
        
        #匹配key1进入下一次循环匹配key2
        if "[%s]" % key1 in line:
            flag = 1
            continue
        if flag == 1:
            #进入下一个key新增key2
            if line[0] == "[" and line[-1] == "]":
                newline = key2 + "=" + val + "\n"
                cfg = cfg[:i] + [newline] + cfg[i:]
                return writeFile(inifile, cfg)
            if line.split("=", 1)[0].strip() == key2: 
                cfg[i] = key2 + "=" + val +"\n"
                return writeFile(inifile,cfg)
    if flag == 1:
        newline = key2 + "=" + val +"\n"
        cfg = cfg + [newline]
        return writeFile(inifile,cfg)
    else:
        #key1不存在时
        cfg = cfg + ["[%s]\n%s=%s"%(key1,key2,val)]
        return writeFile(inifile,cfg)
        
def writeFile(inifile,cfg):
    with open(inifile,"w",encoding = "utf-8") as fp:
        fp.writelines(cfg)


