import argparse
parser = argparse.ArgumentParser()
parser.description='喂我两个数字，我就吐出他们的积'
parser.add_argument("-a","--ParA", help="我是A",type=int)
parser.add_argument("-b","--ParB", help="我是B",type=int)
parser.add_argument('-p', '--project', type=str, default="hert-510c00", help='project name')
parser.add_argument('-M', '--mount-point', type=str, help='mountpoint')
parser.add_argument('-D', '--cache-dir', type=str, help='specific cache dir for client and shell')
parser.add_argument('-C', '--commit-no', type=str, help='specific commit_no')
# parser.add_argument('-b', '--branch', type=str, default="master", help='branch to checkout to')
parser.add_argument('-i', '--build-id', type=str, default="local", help='branch trace info')
parser.add_argument('-v', '--versions', type=str, help='artifact version specific config')
parser.add_argument('-s', '--start-pre', action='store_true', help='whether start pre automatically')
parser.add_argument('-H', '--use-history', action='store_true', help='whether use venom history HEAD')
# parser.add_argument('-c', '--clean', type=str2bool, nargs='?', const=True, default=True, help='whether clean the tmp')
parser.add_argument('-g', '--git-url', type=str, default='http://pihertbbuint:73imoA2uVSZzsdpr9bqL@code-sh.rnd.huawei.com/ROSA_RB/RB_V5R10C00.git', help='git url for clone')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='debug mode')
parser.add_argument('-m', '--manifest', type=str, default="", help='Manifest file for multi repo')

args = parser.parse_args()
if args.ParA:
    print("我只吃到了A，它是",args.ParA)
if args.ParB:
    print("我只吃到了B，它是",args.ParB)
if args.ParA and args.ParB:
    print("啊，两个都吃到啦！积是",args.ParA*args.ParB)
    

arg_dict = vars(args)
print(arg_dict)