import inspect
import traceback
import sys
import datetime
import os
import re

class ConsoleColors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END_CODE = '\033[0m'


class Log:
    TAG = 'Log'

    @staticmethod
    def w(text=''):
        trbk = ''.join(traceback.format_tb(sys.exc_info()[2])).strip()
        if trbk:
            trbk = '\n' + trbk + '\n' + '{0}: {1}'.format(sys.exc_info()[0].__name__, sys.exc_info()[1])
        if text:
            text = text + ' '
        print('{4}{0} Log/W: {1}{2}{3}{5}'.format(Log.getDatetimeStr(), text, Log.getFileInfo(), trbk, ConsoleColors.YELLOW, ConsoleColors.END_CODE))

    @staticmethod
    def e(text=''):
        trbk = ''.join(traceback.format_tb(sys.exc_info()[2])).strip()
        if trbk:
            trbk = '\n' + trbk + '\n' + '{0}: {1}'.format(sys.exc_info()[0].__name__, sys.exc_info()[1])
        if text:
            text = text + ' '
        print('{4}{0} Log/E: {1}{2}{3}{5}'.format(Log.getDatetimeStr(), text, Log.getFileInfo(), trbk, ConsoleColors.RED, ConsoleColors.END_CODE))

    @staticmethod
    def i(text=''):
        if text:
            text = text + ' '
        print('{0} Log/I: {1}{2}'.format(Log.getDatetimeStr(), text, Log.getFileInfo()))

    @staticmethod
    def v(text=''):
        if text:
            text = text + ' '
        print('{0} Log/V: {1}{2}'.format(Log.getDatetimeStr(), text, Log.getFileInfo()))

    @staticmethod
    def d(text=''):
        if text:
            text = text + ' '
        print('{0} Log/D: {1}{2}'.format(Log.getDatetimeStr(), text, Log.getFileInfo()))

    @staticmethod
    def getFileInfo():
        frame = inspect.currentframe().f_back.f_back
        className = '__main__'
        if 'self' in frame.f_locals:
            className = frame.f_locals['self'].__class__.__name__
        return '({0}:{1:d} in {2}#{3})'.format(os.path.basename(frame.f_code.co_filename), frame.f_lineno, className, frame.f_code.co_name)

    @staticmethod
    def getDatetimeStr():
        nowTime = datetime.datetime.now()
        return '{0}.{1:03.0f}'.format(nowTime.strftime('%m-%d %H:%M:%S'), int(nowTime.strftime('%f')) / 1000)
