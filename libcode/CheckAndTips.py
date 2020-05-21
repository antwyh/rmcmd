import os
import sys
import time
import datetime

class CheckAndTips:
    redPrint="\033[31m"
    greenPrint = "\033[32m"
    yellowPrint = "\033[33m"
    bluePrint = "\033[34m"
    yellowLinePrint = "\033[1;4;33m"
    geenLinePrint = "\033[1;4;32m"
    geenBackPrint = "\033[1;4;42m"
    endPrint="\033[0m"
    #red--echo -e "\033[31m${*}\033[0m"
    #green -e "\033[32m${*}\033[0m"
    ##红色打印
    def printRed(str):
        print(CheckAndTips.redPrint, str, CheckAndTips.endPrint)
    def printGreenBash(str):
        print(CheckAndTips.greenPrint, str, CheckAndTips.endPrint, end=' ')
    def printGreen(str):
        print(CheckAndTips.greenPrint, str, CheckAndTips.endPrint)
    def printYellow(str):
        print(CheckAndTips.yellowPrint, str, CheckAndTips.endPrint)
    def printYellowBash(str):
        print(CheckAndTips.yellowPrint, str, CheckAndTips.endPrint, end=' ')
    def printBlue(str):
        print(CheckAndTips.bluePrint, str, CheckAndTips.endPrint)
    def printYellowLine(str):
        print(CheckAndTips.yellowLinePrint, str, CheckAndTips.endPrint)
    def printLine(str):
        print(CheckAndTips.geenLinePrint, str, CheckAndTips.endPrint)

    def printBack(str):
        print(CheckAndTips.geenBackPrint, str, CheckAndTips.endPrint)

    def checkForPrepare(response):
        if (len(response.placeIdList) != 0):
            CheckAndTips.printGreen("\t[操作成功!] 当前课表设备已与云端同步，将使用课表模拟器缓存配置进行操作:")
            return True
        else:
            CheckAndTips.printRed("\t[操作失败!]  请检查课堂数据是否正常! 可根据如下选项检查:")
            return False

    def checkForAddEp(response):
        if (response.code == 204 or response.code == 200):
            CheckAndTips.printGreen("----加入课堂成功:" + str(response.roomVid))
            CheckAndTips.printGreen("回复详情:" + response.info)
            return True
        else:
            CheckAndTips.printRed("----加入课堂失败，请进行检查:" + str(response.roomVid))
            CheckAndTips.printRed("原因:" + response.info)
            return False

    def checkForDelEp(response):
        if (response.code == 204 or response.code == 200):
            CheckAndTips.printGreen("----退出课堂成功:" + str(response.roomVid))
            CheckAndTips.printGreen("回复详情:" + response.info)
            return True
        else:
            CheckAndTips.printRed("----退出课堂失败，请进行检查:" + str(response.roomVid))
            CheckAndTips.printRed("原因:" + response.info)
            return False

    def checkForCameraChange(response):
        if (response.code == 204 or response.code == 200):
            CheckAndTips.printGreen("----开启共享成功:" + str(response.roomVid))
            return True
        else:
            CheckAndTips.printRed("----开启共享失败，请进行检查:" + str(response.roomVid))
            CheckAndTips.printRed("原因:" + response.info)
            return False

    def checkForStartContent(response):
        if (response.code == 204 or response.code == 200):
            CheckAndTips.printGreen("----开启共享成功:" + str(response.roomVid))
            return True
        else:
            CheckAndTips.printRed("----开启共享失败，请进行检查:" + str(response.roomVid))
            CheckAndTips.printRed("原因:" + response.info)
            return False

    def checkForStopContent(response):
        if (response.code == 204 or response.code == 200):
            CheckAndTips.printGreen("----停止共享成功:" + str(response.roomVid))
            return True
        else:
            CheckAndTips.printRed("----停止共享失败，请进行检查:" + str(response.roomVid))
            CheckAndTips.printRed("原因:" + response.info)
            return False
    def checkForInteract(response):
        if (response.code == 204 or response.code == 200):
            CheckAndTips.printGreen("----互动操作成功:" + str(response.roomVid))
            return True
        else:
            CheckAndTips.printRed("----互动操作失败，请进行检查:" + str(response.roomVid))
            CheckAndTips.printRed("原因:" + response.info)
            return False
    def checkForEndClass(response):
        if (response.code == 204 or response.code == 200):
            CheckAndTips.printGreen("----结束课堂成功:" + str(response.roomVid))
            return True
        else:
            CheckAndTips.printRed("----结束课堂失败，请进行检查:" + str(response.roomVid))
            CheckAndTips.printRed("原因:" + response.info)
            return False
    def checkForStopContent(response):
        if (response.code == 204 or response.code == 200):
            CheckAndTips.printGreen("----停止共享成功:" + str(response.roomVid))
            return True
        else:
            CheckAndTips.printRed("----停止共享失败，请进行检查:" + str(response.roomVid))
            CheckAndTips.printRed("原因:" + response.info)
            return False
    def checkResponse(response):
        if (response.code == 204 or response.code == 200):
            return True
        else:
            return False

    def printProcessFormat(cmdStr='', func=None, isPrintOn=True, executeDetail='', successFlag=True):
        print_str = "===========执行开始===========\n";
        print_str += "执行命令  : "+ str(cmdStr) + "\n"
        startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print_str += "执行时间  : " + str(startTime) + "\n"

        if executeDetail is not None and executeDetail != '':
            print_str += "执行时间  : \n" + str(executeDetail) + "\n"
        print_str+="===========执行结束===========\n"
        ################################
        ####最终打印
        if (successFlag is True):
            CheckAndTips.printGreen(print_str)
        else:
            CheckAndTips.printRed(print_str)

class ShowProcess():
    def sleepAndShowProgress(self, sleepTime, tips="ADD"):
        d = 0
        sleepPerTime=sleepTime/10
        for data in range(1, 11):
            time.sleep(sleepPerTime)
            d += 1
            done = int(50 * d / 10)
            sys.stdout.write("\r[%s%s] %d%% --[sleep %s s] [%s]" % ('█' * done,
                                                ' ' * (50 - done), 10 * d, sleepTime, tips))
            sys.stdout.flush()

    def indexShowProgress(self, index, maxVal=100, maxlenth = 50, tips="ADD"):

        for data in range(0, maxVal):
            done = int(maxlenth * index / maxVal)
            percent_sum = index/maxVal*100
            sys.stdout.write("\r[%s%s] %d%% --[Sum:%d - index:%d] [%s]" % ('█' * done,
                                                ' ' * (maxlenth - done), percent_sum, maxVal, index, tips))
            sys.stdout.flush()
    def indexShowProgressRed(self, index, maxVal=100, maxlenth = 50, tips="ADD"):
        for data in range(0, maxVal):
            done = int(maxlenth * index / maxVal)
            percent_sum = index/maxVal*100
            sys.stdout.write("\r\033[31m[%s%s] %d%% --[Sum:%d - index:%d] [%s]\033[0m" % ('█' * done,
                                                ' ' * (maxlenth - done), percent_sum, maxVal, index, tips))
            sys.stdout.flush()
    def indexShowProgressGreen(self, index, maxVal=100, maxlenth = 50, tips="ADD", delayCurrent=float(0)):
        for data in range(0, maxVal):
            done = int(maxlenth * index / maxVal)
            percent_sum = index/maxVal*100

            if (delayCurrent == 0):
                sys.stdout.write("\r\033[32m[%s%s] %d%%[Sum:%d-index:%d][%s]\033[0m " % ('█' * done,
                                                    ' ' * (maxlenth - done), percent_sum, maxVal, index, tips))
            else:
                sys.stdout.write("\r\033[32m[%s%s] %d%%[Sum:%d-index:%d][%s][延迟:%.2f]\033[0m " % ('█' * done,
                         ' ' * (maxlenth - done), percent_sum, maxVal, index, tips, delayCurrent))
            sys.stdout.flush()

if __name__ == '__main__':
    #ShowProcess().sleepAndShowProgress(10, tips='remove')
    index=0;
    max=15;
    CheckAndTips.printProcessFormat(cmdStr="终端呼叫", index=1,flag=True,
                                                roomVid='001', details='001')
    # while(index<max):
    #     index+=1;
    #     time.sleep(1)
    #     ShowProcess().indexShowProgressRed(index, maxVal=max, maxlenth = 100, tips="ADD")

