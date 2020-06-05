import os
import sys
import time
import datetime
from libcode.CheckAndTips import CheckAndTips
class SimulaterOpClass():
    def installPython(self, index=0):
        ###### 01-建立目录
        cmd2 = "rmc scp --index={0} --file=\"client.tar.gz\" --dstpath=\"/root/simulator-docker/\" ;".format(index)
        cmd3 = "rmc dockercmd --index={0} --value=\"cd /root/simulator/log/; tar xf client.tar.gz; rm -fr ../python; mv python-client/ ../python\"".format(index)
        ###############################
        cmdstr= cmd2 + cmd3
        CheckAndTips.printGreen("[提示] 执行如下命令" + cmdstr)
        os.system(cmdstr)

    def installSimulatorTarForSignal(self, index=0):
        ###### 01-建立目录
        cmd2 = "rmc scp --index={0} --file=\"simulator-1.0-SNAPSHOT.tar\" --dstpath=\"/root/simulator-docker/\" ;".format(index)
        cmd3 = "rmc dockercmd --index={0} --value=\"" \
               "cd /root/simulator/python;../simu-bin/stop-simulator-all;" \
               "cd /root/simulator/log/; mv simulator-1.0-SNAPSHOT.tar /root; " \
               "cd /root/; ls -l simulator-1.0-SNAPSHOT.tar; " \
               "cd /root/simulator/; ls -l; rm -fr bin conf cache lib python version.txt simu-bin; pwd; touch a; ls -l;" \
               "cp /root/simulator-1.0-SNAPSHOT.tar /root/simulator/;" \
               "cd /root/simulator/; tar xf simulator-1.0-SNAPSHOT.tar; ls -l;\"".format(index)
        ###############################
        cmdstr= cmd2 + cmd3
        CheckAndTips.printGreen("[提示] 执行如下命令" + cmdstr)
        os.system(cmdstr)
########################################################################
    def processSimulatorWork(self, index=0, ipaddr='172.20.34.221', filename="~/yunnan.tar.gz",
                             isCheck=False, isScp=False, isUninstall=False, isInstall=False):
        if isCheck: self.checkSimulator(index = index)
        if isScp: self.scpSimulator(index=index, ipaddr=ipaddr, filename=filename)
        if isUninstall: self.uninstallSimulator(index=index)
        if isInstall: self.installSimulator(index=index, ipaddr=ipaddr)

    def processSimulatorWorkFuc(self, index, ipaddr, filename,
                             isCheck, isScp, isUninstall, isInstall):
        self.processSimulatorWork(index=index, ipaddr=ipaddr, filename=filename,
                             isCheck=isCheck, isScp=isScp,
                             isUninstall=isUninstall, isInstall=isInstall)


    def checkSimulator(self, index=0):
        ###### 01-删除模拟器镜像及文件
        cmd1 = "./rmc.py cmd --index={0} --value=\"docker container ls -a;\" ;".format(index)
        cmd2 = "./rmc.py dockercmd --index={0} --value=\"ps aux | grep relay; ps aux | grep java;" \
               "./func-simu-client.py check;\" ;".format(index)
        CheckAndTips.printGreen("[提示]执行模拟器检查命令" + cmd1 + cmd2)
        os.system(cmd1+cmd2)

    def scpSimulator(self, index=0, ipaddr='172.20.34.221', filename="~/yunnan.tar.gz"):
        ###### 01-拷贝模拟器
        cmd1 = "scp {0} root@{1}:/root/".format(filename, ipaddr)
        CheckAndTips.printGreen("[提示] 执行模拟器传输命令" + cmd1 + " --索引:" + str(index) + " --地址:" + ipaddr)
        os.system(cmd1)

    def uninstallSimulator(self, index=0):
        ###### 01-删除模拟器镜像及文件
        cmd1 = "./rmc.py cmd --index={0} --value=\"cd /root/xylink; ls -l;" \
                                                 "./stop.sh; echo '完成容器卸载'; docker ps -a; docker images; cd /root/;" \
                                                "rm -fr xylink/; echo '完成删除xylink'; \""\
                                                .format(index)
        CheckAndTips.printGreen("[提示]执行模拟器卸载命令" + cmd1)
        os.system(cmd1)

    def installSimulator(self, index=0, ipaddr='172.20.34.221'):
        ###### 01-建立目录
        cmd1 = "./rmc.py cmd --index={0} --value=\"" \
               "cd /root; ls -l yunnan.tar.gz; tar -xvf yunnan.tar.gz; cd xylink;" \
               "cd /root/xylink; ls -l;" \
               "./install.sh {1};  docker ps -a;\""\
            .format(index, ipaddr)
        CheckAndTips.printGreen("[提示] 执行模拟器容器安装命令" + cmd1)
        os.system(cmd1)
    ###############################
    ###############################
    def switchConfigs(self, index=0, ipaddr='172.20.34.221', filepath="file/core-xylink.yaml",
                      startRoomVid="90000000", startPlaceId="90000000", addNum=60):
        classNums = int(addNum/5)
        ###### 01-建立目录
        cmd1 = "./rmc.py dockercmd --index={0} --value=\"cd conf; rm -fr *; ls\" ;".format(index)
        newfilename = "core-{0}.yaml".format(ipaddr)
        newpath="/root/simulator-docker/{0}".format(newfilename)
        cmd2 = "rmc scp --index={0} --file=\"{1}\" --dstpath=\"{2}\" ;".format(index, filepath, newpath)
        cmd3 = "./rmc.py dockercmd --index={0} --value=\"cp ../log/{1} ./conf/;echo ./conf/{1} > current-conf-file\" ;".format(index, newfilename)
        cmd4 = "./rmc.py dockercmd --index={0} --value=\"" \
               "./func-simu-client.py configs --key=localIP --value={1}; sleep 1;" \
               "./batch-simu-client.py batch-configs --key=start-placeId --value={2};" \
               "./batch-simu-client.py batch-configs --key=start-roomVid --value={3};" \
               "./batch-simu-client.py batch-configs --key=classSumNums --value={4};" \
               "./func-simu-client.py configs ;" \
               "./batch-simu-client.py batch-configs;" \
               "./func-simu-client.py reload --file-path=./conf/{5};" \
               "\" ;".format(index, ipaddr, startPlaceId, startRoomVid, classNums, newfilename)
        ###############################
        cmdstr=cmd1 + cmd2 + cmd3 + cmd4;
        #cmdstr=cmd4;
        CheckAndTips.printGreen("[提示] 执行如下命令" + cmdstr)
        os.system(cmdstr)