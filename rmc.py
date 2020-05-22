#!/usr/local/bin/python3
#####! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
#############! /usr/bin/python3
"""multi-simu-client
    this is grpc test-case simulator client!
Usage:
    rmc install
    rmc copyid [--index=<id>]
    rmc reload
    rmc list
    rmc login  [--index=<id>]
    rmc state [--index=<id>] [--all] [--sum]
    rmc dockercmd  [--index=<id>] [--all] [--value=<cmdstr>] [--dockerkey=<key>] [--workdir=<workdir>]
    rmc cmd  [--index=<id>] [--all] [--value=<cmdstr>]
    rmc scp [--reverse] [--index=<id>] [--all] [--file=<filename>] [--dir=<dirname>] [--dstpath=<dstpath>]
    rmc (-h | --help) [--skip]
Arguments:
    FILE                the files
Options:
    --file-path=<filepath> 加载文件路径
    --index=<id>     from config file index
    --skip          skip for check ip
    --all          show all state
    --sum          show sub sum state
    --value=<cmdstr>          cmd for remote ctr
    --file=<filename>         local file name
    --dir=<dirname>           local dir name
    --dstpath=<dstpath>       dstpath
    --dockerkey=<key>         docker key value
    --workdir=<workdir>       docker work dir
    --reverse                 scp remote to local
Examples:
    a0-查看本地配置:
        查看本地配置: rmc.py list
    a1-远程执行命令:
        批量执行所有命令: rmc.py cmd --all
Tips:
    input the right value
"""
from docopt import docopt
import os
import socket
import datetime
import time
import sys

from prettytable import PrettyTable

from libcode.LoggerUtils import LoggerUtils
from libcode.LoggerUtils import CmdLogger
from libcode.RemoteYamlUtils import RemoteServerDetails, RemoteServerDockerDetails
from libcode.RemoteYamlUtils import YamlUtils
from libcode.CheckAndTips import CheckAndTips
from libcode.FileUtils import FileUtils
logger=LoggerUtils.createLogger(__name__, "log/rmc.log")

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
    ####执行远程命令
    def processRemoteCmd(self):
        cmdstr = self.arguments['--value']
        cmd = 'ifconfig'
        if cmdstr is not None and cmdstr != "" and cmdstr != "ssh":
            cmd = str(cmdstr)
        elif cmdstr == "ssh":
            cmd = " "
        if self.arguments['--all']:
            for simulator in self.remotes:
                try:
                    cmdprefix = "ssh root@" + str(simulator.addr) + " "
                    actualCmd = cmdprefix + "\"" + cmd + "\""
                    CheckAndTips.printYellow("[提示]执行远程命令:" + cmd + " 描述:" + simulator.addr)
                    os.system(actualCmd)
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
    CmdLogger.logCmd(arguments, './rmc.py')
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
    remotes = RemoteServerDetails.listRemoteSimulators(filename)
    remoteControlOp = RemoteControlOption(arguments, remotes=remotes)
    #######################################
    if arguments['copyid']:
        CheckAndTips.printGreen("[提示1] 生成秘钥:ssh-keygen")
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
            #### todo:-t方式登录会使得一些系统变量生效，此处需要优化
            #cmdprefix = "ssh -t root@" + str(simulator.addr) + " \'source ~/.bashrc; cd {0}; bash\'".format(simulator.workdir)
            if (simulator.dockerlogin != ''):
                print(simulator.dockerlogin)
                cmdprefix="ssh root@" + str(simulator.addr) + " \'{0}; bash\'".format(simulator.dockerlogin)
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