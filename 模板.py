import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s:%(message)s',
                    datefmt='%H:%M:%S',
                    )
myfile = os.path.realpath(__file__)
mypath = os.path.dirname(myfile)

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
  
  
  def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]))
    parser.add_argument('-p', '--project', type=str, default="hert-510c00", help='project name')
    parser.add_argument('-M', '--mount-point', type=str, help='mountpoint')
    parser.add_argument('-D', '--cache-dir', type=str, help='specific cache dir for client and shell')
    parser.add_argument('-C', '--commit-no', type=str, help='specific commit_no')
    parser.add_argument('-b', '--branch', type=str, default="master", help='branch to checkout to')
    parser.add_argument('-i', '--build-id', type=str, default="local", help='branch trace info')
    parser.add_argument('-v', '--versions', type=str, help='artifact version specific config')
    parser.add_argument('--push', type=str2bool, nargs='?', const=True, default=True, help='whether need to push')
    parser.add_argument('-s', '--start-pre', action='store_true', help='whether start pre automatically')
    parser.add_argument('-H', '--use-history', action='store_true', help='whether use venom history HEAD')
    parser.add_argument('-c', '--clean', type=str2bool, nargs='?', const=True, default=True, help='whether clean the tmp')
    parser.add_argument('-g', '--git-url', type=str, default='http://pihertbbuint:73imoA2uVSZzsdpr9bqL@code-sh.rnd.huawei.com/ROSA_RB/RB_V5R10C00.git', help='git url for clone')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('-m', '--manifest', type=str, default="", help='Manifest file for multi repo')
    parser.add_argument('--standalone', action='store_true', help='Whether stay alive after start the mount')
    parser.add_argument('--no_base', type=str2bool, nargs='?', const=True, default=True, help="base artifact is required or not")
    parser.add_argument('--artifacts_cluster', type=str2bool, nargs='?', const=False, default=False, help="base artifact is required or not")
    args = parser.parse_args()
    arg_dict = vars(args)
    arg_dict["windows"] = platform.system().lower() == 'windows'
    arg_dict["project"] = arg_dict["project"].lower()
