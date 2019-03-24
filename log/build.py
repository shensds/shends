
import os
import sys
import shutil
import socket
import platform
import xmltodict
import logging.config

MyFile = os.path.realpath(__file__)
MyPath = os.path.dirname(MyFile)

LogPath = os.path.realpath(os.path.join(MyPath, 'logs'))
if not os.path.exists(LogPath):
    os.makedirs(LogPath)

log = logging.getLogger()
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(filename)s line:%(lineno)d %(name)s:%(levelname)s: %(message)s',
                              datefmt='%H:%M:%S')
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
log.addHandler(console_handler)
log.setLevel(logging.DEBUG)
CodePath = os.path.realpath(os.path.join(MyPath, '..'))
OneKeyPath = os.path.realpath(os.path.join(CodePath, 'build', 'onekey'))
sys.path.append(os.path.join(OneKeyPath, 'crsp'))

#import crsp

KWARGS = {}


def _init(argv):
    # Initialize the project path
    global KWARGS

    # Init log file config
    file_handler = logging.FileHandler(os.path.join(LogPath, 'build.log'), 'w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    # with open(os.path.join(MyPath, 'config.xml'), 'r') as f:
    #     cfg = xmltodict.parse(f.read())
    cfg = "wocao"

    if len(argv) > 0 and argv[0].upper() in ['4G', '5G']:
        KWARGS['version'] = argv[0].upper()
    else:
        KWARGS['version'] = cfg["@version"].upper()

    KWARGS['mode'] = cfg["@mode"].lower()
    KWARGS['build_dir'] = MyPath
    KWARGS['CodePath'] = CodePath
    KWARGS['crsp_dir'] = os.path.join(OneKeyPath, 'crsp')

    if KWARGS['version'] == '4G':
        KWARGS['work_dir_win'] = CodePath
        KWARGS['work_dir_linux'] = cfg["linux"]["@codepath"].replace('\\', '/')
        KWARGS['work_dir_mount'] = cfg["mount"]["@mountpath"].replace('\\', '/')
        KWARGS['putty_path'] = cfg["putty"]["@path"]
        KWARGS['linux_passwd'] = cfg["linux"]["@passwd"]
        KWARGS['linux_user'] = cfg["linux"]["@user"]
        KWARGS['linux_ip'] = cfg["linux"]["@ip"]
        KWARGS['linux_port'] = cfg["linux"]["@port"]
        KWARGS['mount_path'] = cfg["mount"]["@mountpath"]
        KWARGS['mount_user'] = cfg["mount"]["@user"]
        KWARGS['mount_passwd'] = cfg["mount"]["@passwd"]
        IP = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        drive, path = os.path.splitdrive(KWARGS['work_dir_win'])
        drive = drive.rstrip(':').lower()
        path = path.replace('\\', '/').lstrip('/')
        KWARGS['mount_srcpath'] = "//{}/{}$/{}".format(IP, drive, path)
    else:
        KWARGS['work_dir_linux'] = CodePath

    log.info("KWARGS['work_dir_win']  : {}".format(KWARGS.get('work_dir_win')))
    log.info("KWARGS['work_dir_linux']: {}".format(KWARGS.get('work_dir_linux')))
    log.info("KWARGS['work_dir_mount']: {}".format(KWARGS.get('work_dir_mount')))
    log.info("KWARGS['version']       : {}".format(KWARGS.get('version')))
    log.info("KWARGS['putty_path']    : {}".format(KWARGS.get('putty_path')))
    log.info("KWARGS['mount_path']    : {}".format(KWARGS.get('mount_path')))
    log.info("KWARGS['mount_srcpath'] : {}".format(KWARGS.get('mount_srcpath')))

    # Initialize the log path
    if os.path.exists(os.path.join(LogPath, 'Win')):
        shutil.rmtree(os.path.join(LogPath, 'Win'))
    if KWARGS['version'] == '4G':
        os.makedirs(os.path.join(LogPath, 'Win'))
    if os.path.exists(os.path.join(LogPath, 'Linux')):
        shutil.rmtree(os.path.join(LogPath, 'Linux'))
    os.makedirs(os.path.join(LogPath, 'Linux'))

    # clean output folder
    output = os.path.realpath(os.path.join(CodePath, 'output', 'project'))
    log.info("Clean output: {}".format(output))
    if os.path.exists(output):
        shutil.rmtree(output)
    os.makedirs(output)


def clean():
    # 清理构建结果
    clean_foledrs = [
        '{}/output/project/',
        '{}/project/build/output/',
        '{}/project/makebin/output/',
        '{}/project/makecomm/output/',
        '{}/build/logs/',
    ]
    for folder in clean_foledrs:
        folder = os.path.realpath(folder.format(CodePath))
        log.info("Clean: {}".format(folder))
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    # 清理中间件
    if platform.system() == 'Windows':
        file = 'clean_up_folder_4g.txt'
    else:
        file = 'clean_up_folder_5g.txt'

    with open(os.path.realpath(os.path.join(OneKeyPath, 'crsp', file)), 'r') as f:
        for folder in [i.strip() for i in f.readlines() if i.strip()]:
            folder = os.path.realpath(os.path.join(CodePath, folder))
            log.info("Clean: {}".format(folder))
            if os.path.isdir(folder):
                shutil.rmtree(folder)
            elif os.path.isfile(folder):
                os.remove(folder)

    if platform.system() == 'Windows':
        cmd = 'del /s /q {}\\hert_bsp\\Source\\CBB_CP\\Build\\Obj\\*.cmd'.format(CodePath)
    else:
        cmd = 'find {}/hert_bsp/Source/CBB_CP/Build/Obj/ -name "*.cmd" | xargs rm -rf'.format(CodePath)
    log.info('Exec Cmd: {}'.format(cmd))
    ret, txt = crsp.get_status_output(cmd)
    if ret != 0:
        log.info(txt)

    return True


def parse_paras(args):
    if len(args) == 1 and args[0] == 'clean':
        return clean()

    elif len(args) == 0 or args[0].upper() in ['4G', '5G']:
        #_init(args)
        return run()

    else:
        return False


def run():
    # Call a one-click script for each component
    global KWARGS

    # select version 4G or 5G?
    version = KWARGS['version']
    if version not in ['4G', '5G']:
        log.error("Version 4g or 5g must be configured.")
        return False

    KWARGS['cmdWinList'] = []
    KWARGS['cmdLinuxList'] = []

    for folder in ['sms', 'bsp', 'tran', 'crsp']:
        # 5G is not running on windows
        if version == '4G':
            with open(os.path.join(OneKeyPath, folder, 'cmdListWin_{}.txt'.format(version)), 'r') as f:
                tmp = [i.strip() for i in f.readlines() if i.strip()]
                KWARGS['cmdWinList'].extend(tmp)
        with open(os.path.join(OneKeyPath, folder, 'cmdListLinux_{}.txt'.format(version)), 'r') as f:
            tmp = [i.strip() for i in f.readlines() if i.strip()]
            KWARGS['cmdLinuxList'].extend(tmp)
    if not crsp.run(KWARGS, LogPath):
        return False
    return True


if __name__ == '__main__':
    logging.info(sys.argv[1:])
    sign = parse_paras(sys.argv[1:])
    if sign:
        logging.info("Run success!")
        sys.exit(0)
    else:
        logging.error("Run failed!")
        sys.exit(1)
