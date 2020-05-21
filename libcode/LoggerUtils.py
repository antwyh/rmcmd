#!/usr/local/bin/python3.7
import logging


class LoggerUtils:
    def __init__(self, name, path):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level = logging.INFO)
        handler = logging.FileHandler(path)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(pathname)s(%(lineno)d): %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def createLogger(name, path):
        return LoggerUtils(name, path).logger

class CmdLogger:
    cmdLoger = LoggerUtils.createLogger(__name__, "log/cmd.log")
    @staticmethod
    def logCmd(arguments, cmd):
        cmdPara = []
        for argob in arguments:
            if arguments[argob] is not False and arguments[argob] is not None:
                if (argob=='--index'):
                    cmdPara.append("{0}:{1}".format(argob, arguments[argob]))
                elif arguments[argob] != 0:
                    cmdPara.append("{0}:{1}".format(argob, arguments[argob]))
        CmdLogger.cmdLoger.info("------------------------------->执行命令[%s]参数如下:\n%s", cmd, cmdPara)