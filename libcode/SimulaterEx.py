import os
import sys
import time
import datetime
from libcode.CheckAndTips import CheckAndTips
class SimulaterOpClass():
    def installPython(self, index=0, ipaddr='172.20.34.221', filepath="file/core-xylink.yaml"):
        ###### 01-建立目录
        cmd1 = "cd /Users/fwd/01-Code/edusimulatorclient/00-python-client/;pwd;tar cf client.tar.gz python-client/; ls -l client.tar.gz;"
        cmd2 = "rmc scp --index={0} --file=\"/Users/fwd/01-Code/edusimulatorclient/00-python-client/client.tar.gz\" --dstpath=\"/root/simulator-docker/\" ;".format(index)
        cmd3 = "rmc dockercmd --index={0} --value=\"cd /root/simulator/log/; tar xf client.tar.gz; rm -fr ../python; mv python-client/ ../python\"".format(index)
        ###############################
        cmdstr=cmd1 + cmd2 + cmd3
        CheckAndTips.printGreen("[提示] 执行如下命令" + cmdstr)
        os.system(cmdstr)

    def installSimulator(self, index=0, ipaddr='172.20.34.221'):
        ###### 01-建立目录
        cmd1 = "./rmc.py cmd --index={0} --value=\"cd /root; mkdir -p 01-tar/;cp /root/yunnan.tar.gz 01-tar;cd 01-tar;" \
               "tar xf yunnan.tar.gz;  \""\
            .format(index)
        cmd2="./install.sh {0}".format(ipaddr)
        CheckAndTips.printGreen("[提示] 执行如下命令" + cmd2)
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