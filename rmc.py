#!/usr/local/bin/python3
#####! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
#############! /usr/bin/python3
"""multi-simu-client
    this is grpc test-case simulator client!
Usage:
    rmc install
    rmc copyid [--index=<id>] [--all]
    rmc reload
    rmc list
    rmc login  [--index=<id>] [--todir]
    rmc dockercmd  [--index=<id>] [--all] [--range=<range>] [--value=<cmdstr>] [--dockerkey=<key>] [--workdir=<workdir>]
    rmc cmd  [--index=<id>] [--all] [--range=<range>] [--value=<cmdstr>] [--future]
    rmc scp [--reverse] [--index=<id>] [--all] [--range=<range>] [--file=<filename>] [--dir=<dirname>] [--dstpath=<dstpath>]
    rmc switch [--index=<id>] [--all] [--file=<filename>] [--roomvid=<roomvid>] [--autoadd=<number>]
    rmc install-docker [--index=<id>] [--all] [--file=<filename>]
    rmc debug [--index=<id>] [--all]
    rmc install-docker [--index=<id>] [--all] [--scp] [--install] [--uninstall] [--check] [--future]
    rmc tarself
    rmc pullself
    rmc ynclear
    rmc rm-docker
    rmc (-h | --help) [--skip]
Arguments:
    FILE                the files
Options:
    --file-path=<filepath> 加载文件路径
    --index=<id>      from config file index
    --skip            skip for check ip
    --all             show all state
    --range=<range>   range index with all
    --sum          show sub sum state
    --todir        to the dst dir
    --value=<cmdstr>          cmd for remote ctr
    --file=<filename>         local file name
    --dir=<dirname>           local dir name
    --dstpath=<dstpath>       dstpath
    --dockerkey=<key>         docker key value
    --workdir=<workdir>       docker work dir
    --reverse                 scp remote to local
    --addnum=<addnum>         id add num
    --roomvid=<roomvid>       roomvid
    --autoadd=<number>        autoadd num
    --future                  concurrent way to execute
    --scp                     scp moni tar
    --install                 install tar
    --uninstall               removte tar and contanier
Examples:
    0-查看本地配置:
        查看本地配置: rmc.py list
    1-远程执行命令:
        批量执行所有命令: rmc.py cmd --all
    2-切换配置文件
        rmc switch  --file=./file/core-example.yaml --all --roomvid=10000000 --autoadd=60
        rmc switch  --file=./file/core-example.yaml --index=1 --roomvid=10000000 --autoadd=70
        rmc switch  --file=./file/core-xylink.yaml --index=0 --roomvid=11010001 --autoadd=70
    3-yunnan清空模拟器环境
        rmc ynclear
    4-批量查看状态
        rmc dockercmd --all --value="./func-simu-client.py state"
    5-云南环境换包
        rmc debug --index=0
        rmc debug --all
Tips:
    input the right value
"""
from docopt import docopt
import os
import socket
from datetime import datetime
import time
import sys
from concurrent import futures
from prettytable import PrettyTable

from libcode.LoggerUtils import LoggerUtils
from libcode.LoggerUtils import CmdLogger
from libcode.RemoteYamlUtils import RemoteServerDetails, RemoteServerDockerDetails
from libcode.RemoteYamlUtils import YamlUtils
from libcode.CheckAndTips import CheckAndTips
from libcode.FileUtils import FileUtils
from libcode.SimulaterEx import SimulaterOpClass
logger=LoggerUtils.createLogger(__name__, "log/rmc.log")
import traceback
from multiprocessing  import Process
MAX_WORKERS = 20

def toScpCmd(addr, fileName=None, dirName=None, reverseDirection=False, dstPath=""):
    cmdstr = ""
    if not reverseDirection:
        if fileName is not None:
            cmdstr = "scp {0} root@{1}:{2}".format(fileName, addr, dstPath)
        elif dirName is not None:
            cmdstr = "scp -r {0} root@{1}:{2}".format(dirName, addr, dstPath)
    else:
        if fileName is not None:
            cmdstr = "scp root@{0}:{1} {2} ".format(addr, fileName, dstPath)
        elif dirName is not None:
            cmdstr = "scp root@{0}:{1} {2} ".format(addr, dirName, dstPath)
    return cmdstr

class RemoteControlOption:
    def __init__(self, arguments, remotes=[]):
        self.arguments = arguments
        self.remotes = remotes
    @staticmethod
    def listRemoteControllers(remotes='', cmdStr='查看服务器配置列表'):
        printstr=''
        xtable = PrettyTable(["索引", "地址", "描述", "密码", "目录"])
        xtable.align["行号"] = "|"  # Left align city names
        xtable.padding_width = 0  # One space between column edges and contents (default)
        for remoteSimu in remotes:
            xtable.add_row([remoteSimu.index, remoteSimu.addr, remoteSimu.detail, remoteSimu.passwd, remoteSimu.workdir])
        CheckAndTips.printProcessFormat(cmdStr, executeDetail=str(xtable))

    ####远程拷贝秘钥
    def processRemoteCopySshId(self):
        pubfile = self.arguments['--file']
        pubfilename="~/.ssh/id_rsa.pub"
        if pubfile is not None and pubfile != "":
            pubfilename = pubfile
        if self.arguments['--all']:
            for simulator in self.remotes:
                try:
                    cmdprefix = "ssh-copy-id -i " + pubfilename +  " root@" + str(simulator.addr) + " "
                    CheckAndTips.printYellow("[提示]执行复制秘钥命令:" + cmdprefix + " 描述:" + simulator.addr)
                    os.system(cmdprefix)
                except Exception as e:
                    CheckAndTips.printRed("[错误] 执行复制秘钥命令失败，请检查配置- " + simulator.addr)
                    CheckAndTips.printRed("\n\n\n")
        else:
            index=0
            id = self.arguments['--index']
            if id is not None:
                index= int(id)
            try:
                simulator = self.remotes[index]
                cmdprefix = "ssh-copy-id -i " + pubfilename + " root@" + str(simulator.addr)
                CheckAndTips.printYellow("[提示]执行复制秘钥命令:" + cmdprefix + " 描述:" + simulator.addr)
                os.system(cmdprefix)
            except Exception as e:
                CheckAndTips.printRed("[错误] 执行复制秘钥命令失败，请检查配置- " + simulator.addr)
                CheckAndTips.printRed("\n\n\n")
    @staticmethod
    def sysExcute(cmd):
        os.system(cmd)
    ####执行远程命令
    def processRemoteCmd(self):
        cmdstr = self.arguments['--value']
        cmd = 'ifconfig'
        if cmdstr is not None and cmdstr != "" and cmdstr != "ssh":
            cmd = str(cmdstr)
        elif cmdstr == "ssh":
            cmd = " "
        if self.arguments['--all']:
            starttime=datetime.utcnow().strftime('%Y-%m-%d-%H:%M:%S.%f')[:-3]
            #with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for simulator in self.remotes:
                try:
                    cmdprefix = "ssh root@" + str(simulator.addr) + " "
                    actualCmd = cmdprefix + "\"" + cmd + "\""
                    CheckAndTips.printYellow("[提示]执行远程命令:" + cmd + " 描述:" + simulator.addr)
                    if (not self.arguments['--future']):
                        os.system(actualCmd)
                    else:
                        # Start the load operations and mark each future with its URL
                        CheckAndTips.printYellow("[提示] 异步执行命令" + actualCmd)
                        #executor.submit(RemoteControlOption.sysExcute, actualCmd)
                        ps = Process(target=RemoteControlOption.sysExcute, args=(actualCmd,))
                        print("---》##### ps pid: " + str(ps.pid) + ", ident:" + str(ps.ident))
                        ps.start()

                except Exception as e:
                    CheckAndTips.printRed("[错误] 执行远程命令失败，请检查ssh配置- " + simulator.addr)
                    CheckAndTips.printRed("\n\n\n")
            print("--start:", starttime)
            print("----end:", datetime.utcnow().strftime('%Y-%m-%d-%H:%M:%S.%f')[:-3])
        else:
            index=0
            id = self.arguments['--index']
            if id is not None:
                index= int(id)
            try:
                simulator = self.remotes[index]
                cmdprefix = "ssh root@" + str(simulator.addr) + " "
                actualCmd = cmdprefix + "\"" + cmd + "\""
                CheckAndTips.printYellow("[提示]执行远程命令:" + cmd + " 描述:" + simulator.addr)
                os.system(actualCmd)
            except Exception as e:
                CheckAndTips.printRed("[错误] 执行远程命令失败，请检查ssh配置- " + simulator.addr)
                CheckAndTips.printRed("\n\n\n")

    ####执行远程docker命令
    def processDockerRemoteCmd(self, cmd = 'ifconfig', dockerkey="yunnan",workdirstr="/root/simulator/python"):
        cmdstr = self.arguments['--value']
        if cmdstr is not None and cmdstr != "" and cmdstr != "ssh": cmd = str(cmdstr)
        elif cmdstr == "ssh": cmd = " "

        keystr = self.arguments['--dockerkey']
        if keystr is not None and keystr != "": dockerkey = keystr

        dirstr = self.arguments['--workdir']
        if dirstr is not None and dirstr != "": workdirstr = dirstr

        if self.arguments['--all']:
            for simulator in self.remotes:
                try:
                    CheckAndTips.printGreen("\n-----------------------------------------------------")
                    dockerCmd1 = "ssh root@{0} \" docker ps | grep {1} | grep -v grep \"".format(simulator.addr,
                                                                                                 dockerkey)
                    CheckAndTips.printYellow("[提示]执行远程命令:" + dockerCmd1 + " 描述:" + simulator.addr)
                    back1 = os.popen(dockerCmd1).read()
                    dockerId = str(back1).split(" ")[0]
                    if dockerId is None or dockerId == "":
                        CheckAndTips.printRed("[错误]远程容器ID为空,退出本次执行 " + simulator.addr)
                        continue
                    CheckAndTips.printGreen("[提示]远程容器ID为:" + dockerId)
                    dockerCmd2 = "ssh root@{0} \"docker exec -i {1} /bin/bash -c 'cd {2};{3}'\"".format(simulator.addr,
                                                                                                        dockerId,
                                                                                                        workdirstr, cmd)
                    CheckAndTips.printYellow("[提示]执行远程命令:" + dockerCmd2 + " 描述:" + simulator.addr)
                    os.system(dockerCmd2)

                except Exception as e:
                    CheckAndTips.printRed("[错误] 执行远程命令失败，请检查ssh配置- " + simulator.addr)
                    CheckAndTips.printRed("\n\n\n")
        else:
            index=0
            id = self.arguments['--index']
            if id is not None:
                index= int(id)
            try:
                simulator = self.remotes[index]
                dockerCmd1 = "ssh root@{0} \" docker ps | grep {1} | grep -v grep \"".format(simulator.addr, dockerkey)
                CheckAndTips.printYellow("[提示]执行远程命令:" + dockerCmd1 + " 描述:" + simulator.addr)
                back1 = os.popen(dockerCmd1).read()
                dockerId=str(back1).split(" ")[0]
                if dockerId is None or dockerId == "":
                    CheckAndTips.printRed("[错误]远程容器ID为空,退出本次执行 " + simulator.addr)
                    return
                CheckAndTips.printGreen("[提示]远程容器ID为:" + dockerId)
                dockerCmd2 = "ssh root@{0} \"docker exec -i {1} /bin/bash -c 'cd {2};{3}'\"".format(simulator.addr,dockerId,workdirstr,cmd)
                CheckAndTips.printYellow("[提示]执行远程命令:" + dockerCmd2 + " 描述:" + simulator.addr)
                os.system(dockerCmd2)
            except Exception as e:
                CheckAndTips.printRed("[错误] 执行远程命令失败，请检查ssh配置- " + simulator.addr)
                CheckAndTips.printRed("\n\n\n")

    #######################################
    ####远程scp
    def processRemoteScp(self):
        fileName = self.arguments['--file']
        dirName = self.arguments['--dir']
        dstPath = self.arguments['--dstpath']
        if dstPath is None: dstPath = ""
        reverseDirection = self.arguments['--reverse']
        if reverseDirection is not True: reverseDirection = False
        if (fileName is None or fileName == "") and (dirName is None or dirName == ""):
            CheckAndTips.printRed("[错误] 传送文件或者路径为空,直接退出！")
            exit(-1)
        if self.arguments['--all']:
            for simulator in self.remotes:
                try:
                    cmd = toScpCmd(simulator.addr, fileName=fileName, dirName=dirName,
                                   reverseDirection=reverseDirection, dstPath=dstPath)
                    CheckAndTips.printYellow("[提示]执行scp拷贝命令:" + cmd + " 描述:" + simulator.addr)
                    os.system(cmd)
                except Exception as e:
                    CheckAndTips.printRed("[错误] 执行远程拷贝命令失败，请检查ssh配置- " + simulator.addr)
                    CheckAndTips.printRed("\n\n\n")
        else:
            index = 0
            id = self.arguments['--index']
            if id is not None:
                index = int(id)
            try:
                simulator = self.remotes[index]
                cmd = toScpCmd(simulator.addr, fileName=fileName, dirName=dirName, reverseDirection=reverseDirection,
                               dstPath=dstPath)
                CheckAndTips.printYellow("[提示]执行scp拷贝命令:" + cmd + " 描述:" + simulator.addr)
                os.system(cmd)
            except Exception as e:
                CheckAndTips.printRed("[错误] 执行远程拷贝命令失败，请检查ssh配置- " + simulator.addr)
                CheckAndTips.printRed("\n\n\n")
                print(e)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='2.0.0')
    CmdLogger.logCmd(arguments, 'rmc.py')
    if arguments['install']:
        workdir = os.getcwd()
        CheckAndTips.printYellow("[提示] 系统将直接进行远程控制安装设置与检查:" + workdir)
        if (not FileUtils().findstring(os.environ['HOME'] + "/.bashrc", workdir)):
            os.system("echo 'export PATH=$PATH:" + str(workdir) + "' >> ~/.bashrc && source ~/.bashrc")
            CheckAndTips.printYellow("[设置01] 将当前路径加入系统路径, 若未生效请手动输入source ~/.bashrc进行设置")
        exit(1)
    if arguments['reload']:
        CheckAndTips.printYellow("[提示] 系统将重新将在配置文件")
        yamlPath = YamlUtils.listAndChooseConf()
        CheckAndTips.printYellow("[提示] 系统将使用如下配置文件:" + yamlPath)
        exit(1)
    filename=YamlUtils.readCache()
    ####print("-----> 从./current-conf-file读取当前使用配置文件:", filename)
    utils = YamlUtils()
    dockerConfigs=RemoteServerDockerDetails.readRemoteServerDockerDetails(filename)
    remotesValues = RemoteServerDetails.listRemoteSimulators(filename)
    remotes = []
    rangestr = arguments['--range']
    if rangestr is not None and rangestr != "" and "-" in rangestr:
        start = int(rangestr.split("-")[0])
        end  = int(rangestr.split("-")[1])
        CheckAndTips.printGreen("[提示] 选定一定范围索引, -起始:" + str(start) + "-结束:" + str(end))
        index=0
        for remote in remotesValues:
            if index < start: index+=1; continue
            elif index > end: break
            else: index+=1; remotes.append(remote); continue
    else:
        remotes.extend(remotesValues)

    remoteControlOp = RemoteControlOption(arguments, remotes=remotes)
    #######################################
    if arguments['copyid']:
        CheckAndTips.printGreen("[提示1] 生成秘钥:ssh-keygen  安装copy工具：yum -y install openssh-clients")
        CheckAndTips.printGreen("[提示2] 公钥上传:ssh-copy-id -i ~/.ssh/id_rsa.pub root@服务器ip")
        remoteControlOp.processRemoteCopySshId()
        exit(1)
    #######################################
    if arguments['list']:
        RemoteControlOption.listRemoteControllers(remotes=remotes)
    #######################################
    elif arguments['login']:
        index = 0
        id = arguments['--index']
        if id is None:
            RemoteControlOption.listRemoteControllers(remotes=remotes, cmdStr="登录列表展示")
            CheckAndTips.printRed("[提示] 请输入rmc login --index=[index] 登录指定服务器")
        else:
            index=int(id)
            simulator = remotes[index]
            CheckAndTips.printYellow("[提示]将远程登录如下ip: " + simulator.addr)
            cmdprefix = "ssh root@" + str(simulator.addr)
            if (arguments['--todir']):
                cmdprefix = "ssh -t root@" + str(simulator.addr) + " \'source ~/.bashrc; cd {0}; bash\'".format(simulator.workdir)
            #### todo:-t方式登录会使得一些系统变量生效，此处需要优化
            if (simulator.dockerlogin != ''):
                print(simulator.dockerlogin)
                cmdprefix="ssh -t root@" + str(simulator.addr) + " \'{0}; bash\'".format(simulator.dockerlogin)
            os.system(cmdprefix)
    #######################################
    elif arguments['cmd']:
        remoteControlOp.processRemoteCmd()
    #######################################
    elif arguments['scp']:
        remoteControlOp.processRemoteScp()
    elif arguments['dockercmd']:
        if(dockerConfigs is None or dockerConfigs.dockerkey =='' or dockerConfigs.workdir == ''):
            remoteControlOp.processDockerRemoteCmd()
        else:
            remoteControlOp.processDockerRemoteCmd(dockerkey=dockerConfigs.dockerkey, workdirstr=dockerConfigs.workdir)
    elif arguments['switch']:
        configFile = arguments['--file']
        if configFile is None: dstPath = ""
        roomvid = arguments['--roomvid']
        if roomvid is None: roomvid = ""
        addnum=60
        autonum = arguments['--autoadd']
        if autonum is not None and autonum != "":
            addnum=int(autonum)

        CheckAndTips.printGreen("[提示]远程执行配置文件切换")
        simulaterop = SimulaterOpClass()
        if (roomvid is not None and roomvid != ""):
            startRoomVid = int(roomvid)
        if arguments['--all']:
            index=0;
            for simulator in remotes:
                try:
                    CheckAndTips.printYellow(
                        "===========================================================\n"
                        "[提示] 开始进行批量容器操作， 索引:" + str(index) + " 地址:" + simulator.addr)
                    if(roomvid is not None and roomvid != ""):
                        simulaterop.switchConfigs(index=index, ipaddr=simulator.addr, filepath=configFile,
                                                  startRoomVid=startRoomVid, startPlaceId=startRoomVid, addNum=addnum)
                        startRoomVid += addnum;
                    else:
                        simulaterop.switchConfigs(index=index, ipaddr=simulator.addr, filepath=configFile)
                    index+=1
                except Exception as e:
                    traceback.print_exc()
                    CheckAndTips.printRed("[错误] 替换配置文件失败: " + simulator.addr)
                    CheckAndTips.printRed("\n\n\n")
        else:
            index=0
            id = arguments['--index']
            if id is not None:
                index= int(id)
            try:
                simulator = remotes[index]
                CheckAndTips.printYellow("===========================================================\n"
                                         "[提示] 开始进行远程配置文件切换， 索引:" + str(index))
                if (roomvid is not None and roomvid != ""):
                    simulaterop.switchConfigs(index=index, ipaddr=simulator.addr, filepath=configFile,
                                              startRoomVid=startRoomVid, startPlaceId=startRoomVid, addNum=addnum)
                    startRoomVid += 60;
                else:
                    simulaterop.switchConfigs(index=index, ipaddr=simulator.addr, filepath=configFile)
            except Exception as e:
                traceback.print_exc()
                CheckAndTips.printRed("[错误] 替换配置文件失败: " + simulator.addr)
                CheckAndTips.printRed("\n\n\n")
##############################################
    elif arguments['install-docker']:
        CheckAndTips.printGreen("[提示] 远程下载地址：wget http://devcdn.xylink.com/private_cloud/v3.8/deploy/1%2bN/yunnan.tar.gz")
        CheckAndTips.printGreen("[提示]远程进行容器安装")
        if arguments['--all']:
            index=0;
            for simulator in remotes:
                try:
                    cmdprefix = "ssh root@" + str(simulator.addr) + " "
                    CheckAndTips.printYellow(
                        "===========================================================\n"
                        "[提示] 开始进行远程容器传输python安装包， 索引:" + str(index))
                    if (not arguments['--future']):
                        SimulaterOpClass().processSimulatorWork(index=index, ipaddr=simulator.addr,
                                                                isCheck=arguments['--check'], isScp=arguments['--scp'],
                                                                isUninstall=arguments['--uninstall'],
                                                                isInstall=arguments['--install'])
                    else:
                        # Start the load operations and mark each future with its URL
                        CheckAndTips.printYellow("[提示] 异步执行命令")
                        #executor.submit(RemoteControlOption.sysExcute, actualCmd)
                        ps = Process(target=SimulaterOpClass().processSimulatorWorkFuc, args=(index, simulator.addr, "~/yunnan.tar.gz",
                                                                arguments['--check'], arguments['--scp'],
                                                                arguments['--uninstall'],
                                                                arguments['--install']))
                        print("---》##### ps pid: " + str(ps.pid) + ", ident:" + str(ps.ident))
                        ps.start()
                    index+=1
                except Exception as e:
                    traceback.print_exc()
                    CheckAndTips.printRed("[错误] 替换配置文件失败: " + simulator.addr)
                    CheckAndTips.printRed("\n\n\n")
        else:
            index=0
            id = arguments['--index']
            if id is not None:
                index= int(id)
            try:
                simulator = remotes[index]
                SimulaterOpClass().processSimulatorWork(index=index, ipaddr=simulator.addr,
                                     isCheck=arguments['--check'], isScp=arguments['--scp'],
                                     isUninstall=arguments['--uninstall'], isInstall=arguments['--install'])
            except Exception as e:
                traceback.print_exc()
                CheckAndTips.printRed("[错误] 替换配置文件失败: " + simulator.addr)
                CheckAndTips.printRed("\n\n\n")


##############################################
    elif arguments['debug']:
        CheckAndTips.printGreen("[提示] 远程容器传输python安装包")
        if arguments['--all']:
            index=0;
            for simulator in remotes:
                try:
                    cmdprefix = "ssh root@" + str(simulator.addr) + " "
                    CheckAndTips.printYellow(
                        "===========================================================\n"
                        "[提示] 开始进行远程容器传输python安装包， 索引:" + str(index))
                    simulaterop = SimulaterOpClass()
                    simulaterop.installSimulatorTarForSignal(index=index)
                    index+=1
                except Exception as e:
                    traceback.print_exc()
                    CheckAndTips.printRed("[错误] 替换配置文件失败: " + simulator.addr)
                    CheckAndTips.printRed("\n\n\n")
        else:
            index=0
            id = arguments['--index']
            if id is not None:
                index= int(id)
            try:
                simulator = remotes[index]
                CheckAndTips.printYellow("===========================================================\n"
                        "[提示] 开始进行远程容器传输python安装包， 索引:" + str(index))
                simulaterop = SimulaterOpClass()
                simulaterop.installSimulatorTarForSignal(index=index)
            except Exception as e:
                traceback.print_exc()
                CheckAndTips.printRed("[错误] 替换配置文件失败: " + simulator.addr)
                CheckAndTips.printRed("\n\n\n")

    elif arguments['tarself']:
        os.system("cp /Users/fwd/01-Code/edusimulatorclient/rpmbuild/simulator-1.0-SNAPSHOT.tar ./; ls -l simulator-1.0-SNAPSHOT.tar;"
                  "cd ../; tar cf rmc.tar.gz 07-rmcmd/; ls -l rmc.tar.gz")
        cmd1 = "ossutil64 cp -f /tmp/rmc.tar.gz oss://ainemodevcn/private_cloud/v3.8/deploy/1+N/"
        cmdstr="cd ../; scp rmc.tar.gz root@172.18.225.112:/tmp/; ssh root@172.18.225.112 \"{0} \"".format(cmd1)
        CheckAndTips.printYellow("[提示] 执行如下命令：" + cmdstr)
        os.system(cmdstr)

    elif arguments['pullself']:
        os.system("")
    elif arguments['ynclear']:
        os.system("rmc dockercmd --all --value=\"../simu-bin/clear-media-recv\"")