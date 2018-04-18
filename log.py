import inspect
import traceback
import sys
import datetime
import os
import re
from enum import IntEnum

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
    class Level(IntEnum):
        ALL = -1
        DEBUG = 0
        VERBOSE = 1
        VERB = VERBOSE
        INFO = 2
        WARNING = 3
        WARN = WARNING
        ERROR = 4

    TAG = 'Log'
    __level__ = Level.ALL

    @staticmethod
    def set_level(level):
        Log.__level__ = level

    @staticmethod
    def w(text=''):
        if Log.__level__ >= 0 and Log.__level__ > Log.Level.WARN:
            return
        trbk = ''.join(traceback.format_tb(sys.exc_info()[2])).strip()
        if trbk:
            trbk = '\n' + trbk + '\n' + '{0}: {1}'.format(sys.exc_info()[0].__name__, sys.exc_info()[1])
        if text:
            text = text + ' '
        sys.stderr.write('{5}{0} {1}/W: {2}{3}{4}{6}\n'.format(Log.getDatetimeStr(), Log.TAG, text, Log.getFileInfo(), trbk, ConsoleColors.YELLOW, ConsoleColors.END_CODE))

    @staticmethod
    def e(text=''):
        if Log.__level__ >= 0 and Log.__level__ > Log.Level.ERROR:
            return
        trbk = ''.join(traceback.format_tb(sys.exc_info()[2])).strip()
        if trbk:
            trbk = '\n' + trbk + '\n' + '{0}: {1}'.format(sys.exc_info()[0].__name__, sys.exc_info()[1])
        if text:
            text = text + ' '
        sys.stderr.write('{5}{0} {1}/E: {2}{3}{4}{6}\n'.format(Log.getDatetimeStr(), Log.TAG, text, Log.getFileInfo(), trbk, ConsoleColors.RED, ConsoleColors.END_CODE))

    @staticmethod
    def i(text=''):
        if Log.__level__ >= 0 and Log.__level__ > Log.Level.INFO:
            return
        if text:
            text = text + ' '
        print(Log.__level__)
        sys.stderr.write('{0} {1}/I: {2}{3}\n'.format(Log.getDatetimeStr(), Log.TAG, text, Log.getFileInfo()))

    @staticmethod
    def v(text=''):
        if Log.__level__ >= 0 and Log.__level__ > Log.Level.VERBOSE:
            return
        if text:
            text = text + ' '
        sys.stderr.write('{0} {1}/V: {2}{3}\n'.format(Log.getDatetimeStr(), Log.TAG, text, Log.getFileInfo()))

    @staticmethod
    def d(text=''):
        if Log.__level__ >= 0 and Log.__level__ > Log.Level.DEBUG:
            return
        if text:
            text = text + ' '
        sys.stderr.write('{0} {1}/D: {2}{3}\n'.format(Log.getDatetimeStr(), Log.TAG, text, Log.getFileInfo()))

    @staticmethod
    def s(text=''):
        if text:
            text = text + ' '
        sys.stderr.write('{0} {1}/LOG: {2}{3}\n'.format(Log.getDatetimeStr(), Log.TAG, text, Log.getFileInfo()))

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

