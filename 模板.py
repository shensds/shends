import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
import subprocess
def getstatusoutput(cmd):
    """
    Purpose:
    Globals:
    Arguments:
    Returns:
    """
    cmd_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cmd_echo = cmd_process.stdout.read()
    cmd_process.stdout.close()
    sts = cmd_process.wait()
    try:
        cmd_echo = cmd_echo.decode('UTF-8')
    except UnicodeDecodeError:
        cmd_echo = cmd_echo.decode('gbk', errors='ignore')
    if int(platform.python_version().split('.')[0]) < 3:
        if platform.system() == 'Windows':
            cmd_echo = cmd_echo.encode('gbk', errors='ignore')
        else:
            cmd_echo = cmd_echo.encode('UTF-8', errors='ignore')
    if cmd_echo[-1:] == '\n': cmd_echo = cmd_echo[:-1]
    return sts, cmd_echo
        
def readCfg(iniFile):
    cfg = {}
    config = ConfigParser.ConfigParser()
    config.readfp(open(iniFile))
    for section in config.sections():
        cfg[section] = {}
        for option in config.options(section):
            cfg[section][option] = config.get(section, option)
            print("cfg[%s][%s] = %s" % (section, option, config.get(section, option)))
    return cfg
    
def getCreateTime(dir):
    createTime = os.path.getctime(dir)
    createTime = time.localtime(createTime)
    createTime = time.strftime('%Y-%m-%d %X', createTime)
    return createTime
    return time.strftime('%Y-%m-%d %X',time.localtime(time.time()))