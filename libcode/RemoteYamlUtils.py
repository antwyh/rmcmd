import yaml
import time
from datetime import datetime
import os
import socket
from libcode.CheckAndTips import CheckAndTips
class YamlUtils:
    cache_file='current-conf-file'
    @staticmethod
    def showAndChooseConfig():
        CheckAndTips.printRed("==================================================")
        CheckAndTips.printRed("[警告] 检测到本地ip：" + YamlUtils.getHost() + " 与配置文件不符合")
        CheckAndTips.printRed("[提示] 请用户根据测试需求选择适合配置文件!")
        CheckAndTips.printRed("[提示] 配置文件名包含ip仅为防止用户误操作选择其他主机文件!")
        CheckAndTips.printRed("==================================================")
        filename=YamlUtils.listAndChooseConf(localIp=YamlUtils.getHost())
        CheckAndTips.printGreen("[结果] 最终读取配置文件:" + filename)
        CheckAndTips.printGreen("==================================================")
        return filename

    @staticmethod
    def getSettingPath():
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # # 获取本机ip
        ipaddr = socket.gethostbyname(hostname)
        path= "../conf/setting-"+ipaddr+".properties"
        if os.path.exists(path) is True:
            return path
        else:
            return "../conf/setting.properties"
    @staticmethod
    def getHost():
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # # 获取本机ip
        ipaddr = socket.gethostbyname(hostname)
        return ipaddr
    @staticmethod
    def checkFileForHost(fileName):
        ipaddr = YamlUtils.getHost()
        if (ipaddr in fileName):
            return True
        else:
            return False
        # # 获取本机ip
        # ip = socket.gethostbyname(hostname)
    @staticmethod
    def readCache():
        file_obj = open(YamlUtils.cache_file, 'r')
        fileName=file_obj.read()
        file_obj.close()
        return fileName

    @staticmethod
    def writeCache(fileName):
        file_obj = open(YamlUtils.cache_file, 'w')
        file_obj.write(fileName)
        file_obj.close()

    @staticmethod
    def listAndChooseConf(localIp=''):
        file_name = ""
        flag = False
        #while(not YamlUtils.checkFileForHost(file_name)):
        while (not flag):
            index = 0
            listConf = os.listdir("./conf/")
            print("[查看模板] 请查看配置文件列表:")
            print("==================================================")
            tochooseFile=[]
            for configFile in listConf:
                if (localIp != '' and not localIp in configFile):
                    continue
                print("\t{0}) {1}".format(index, configFile))
                tochooseFile.append(configFile)
                index += 1
            print("==================================================")
            print("[选择模板] 请选择序号:", end='')
            line = input()
            print("==================================================")
            if (line.isdigit() and int(line) < len(tochooseFile)):
                file_name='./conf/' + tochooseFile[int(line)]
                YamlUtils.writeCache(file_name)
            else:
                file_name='./conf/003-work-私有云环境-example.yaml'
                YamlUtils.writeCache(file_name)
            flag=True
        return file_name

'''
remote-server-configs:
  dockerbash:
    container-key: "yunnan_moni:1.0"
    container-dir: "/root/simulator/python/"
'''
class RemoteServerDockerDetails():
    #####列出所有id
    @staticmethod
    def readRemoteServerDockerDetails(path):
        with open(path, "r") as yaml_file:
            yaml_obj = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)
            if 'dockerbash' not in yaml_obj['remote-server-configs']:
                return None
            dockerObj = yaml_obj['remote-server-configs']['dockerbash']
            key = '';dir = '/root/';
            for ob in dockerObj:
                if 'container-key' in ob: key= dockerObj['container-key'];
                if 'container-dir' in ob: dir = dockerObj['container-dir'];
            remoteSimulatorDetails = RemoteServerDockerDetails(workdir=dir,dockerkey=key)
            return remoteSimulatorDetails
    def __init__(self, dockerkey='', workdir=''):
        self.dockerkey=dockerkey
        self.workdir=workdir

class RemoteServerDetails():
    #####列出所有id
    @staticmethod
    def listRemoteSimulators(path):
        listRemote = []
        with open(path, "r") as yaml_file:
            yaml_obj = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)
            listObj = yaml_obj['remote-server-configs']['remote-list']
            index=0
            for ob in listObj:
                passwd=''
                if 'passwd' in ob: passwd=ob['passwd']
                workdir='~/'
                if 'workdir' in ob: workdir = ob['workdir']
                dockerlogin=''
                if 'dockerlogin' in ob: dockerlogin=ob['dockerlogin']
                remoteSimulatorDetails = RemoteServerDetails(index=index, addr=ob['addr'],
                            detail=ob['detail'], passwd=passwd, workdir=workdir, dockerlogin=dockerlogin)
                index+=1
                listRemote.append(remoteSimulatorDetails)
        return listRemote
    def __init__(self, index=0, addr='', detail='', cmdstr='', passwd='', workdir='',dockerlogin=''):
        self.index=index
        self.addr=addr
        self.cmdstr=cmdstr
        self.detail=detail
        self.passwd=passwd
        self.workdir=workdir
        self.dockerlogin=dockerlogin