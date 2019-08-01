import os
import subprocess
def get_status_output(cmd):
    """Exec command Returns the status and output after execution"""
    pipe = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = pipe.communicate(input=b'y')[0]
    try:
        out = out.decode('UTF-8')
    except UnicodeDecodeError:
        out = out.decode('gbk', errors='ignore')

    try:
        pipe.kill()
    except OSError:
        pass
    return pipe.returncode, out
    
def saveSymbol(file):
    U =[]
    T =[]
    
    ret,text = get_status_output("nm %s"%file)
    if ret != 0:
        return False
    for line in text.split("\n"):
        if " U " in line:
            U.append(line.split(" U ")[-1])
        elif " T " in line:
            T.append(line.split(" T ")[-1])
    with open(so_file,"a+") as fp:
        fp.write("\n\n%s:\n"%file)
        for i in U:
            fp.write("U %s\n"%i)
        for i in T:
            fp.write("T %s\n"%i)
            
dirlist = [
    "/usr/lib/gcc/x86_64-redhat-linux/4.8.2",
    "jvm/java-1.7.0-openjdk-1.7.0.171-2.6.13.2.el7.x86_64/jre/lib/amd64"
    ]
so_file = "so.txt"
filetype = ["so","a","o"]
    
projectPath = "/usr/lib/"

so_list = []

for dir in dirlist:
    if not dir.startswith("/"):
        dir = os.path.join(projectPath,dir)
    files = os.listdir(dir)
    
    for file in files:
        #跳过非库文件
        if file.split(".")[-1] not in filetype:
            continue
        so_list.append(os.path.join(dir,file))
        
for i in so_list:
    saveSymbol(i)
    

    
    
    
    
    