# coding=utf8
import os


# import tkFileDialog
class FileUtils:
    def readFilename(self, file_dir):
        for root, dirs, files in os.walk(file_dir):
            return files, dirs, root


    def findstring(self, pathfile, keyworld):
        fp = open(pathfile, "r", encoding='UTF-8')  # 注意这里的打开文件编码方式
        strr = fp.read()
        # print strr.find("DoubleVec")
        if (strr.find(keyworld) != -1):
            return True
        return False


    def startfind(self, files, dirs, root):
        for ii in files:
            # print(ii)
            # if ii.endswith('.lua'):
            try:
                if (self.findstring(root + "\\" + ii)):
                    print(ii)
            except Exception as err:
                print(err)
                continue

        for jj in dirs:
            fi, di, ro = self.readFilename(root + "\\" + jj)
            self.startfind(fi, di, ro)