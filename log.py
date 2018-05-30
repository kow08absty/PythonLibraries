import inspect
import traceback
import sys
import datetime
import os
from enum import IntEnum

import colorama

colorama.init()


class ConsoleColors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
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
    _level = Level.ALL
    _show_full_cls = False

    @classmethod
    def set_level(cls, level):
        Log._level = level

    @classmethod
    def set_show_full_class_name(cls, b: bool = False):
        Log._show_full_cls = b

    @classmethod
    def w(cls, content: object = None):
        if Log._level >= 0 and Log._level > Log.Level.WARN:
            return
        trbk = ''.join(traceback.format_tb(sys.exc_info()[2])).strip()
        if trbk:
            trbk = '\n' + trbk + '\n' + '{0}: {1}'.format(sys.exc_info()[0].__name__, sys.exc_info()[1])
        if content:
            content = '%s ' % content
        if Log._show_full_cls:
            class_name = Log.get_full_class_name()
        else:
            class_name = Log.get_simple_class_name()
        sys.stderr.write('{6}{0} {1} {2}/W {3}{4}{5}{7}\n'.format(
            Log.get_datetime_str(), class_name, Log.TAG, content, Log.get_file_info(), trbk,
            ConsoleColors.YELLOW, ConsoleColors.END_CODE
        ))

    @classmethod
    def e(cls, content: object = None):
        if Log._level >= 0 and Log._level > Log.Level.ERROR:
            return
        trbk = ''.join(traceback.format_tb(sys.exc_info()[2])).strip()
        if trbk:
            trbk = '\n' + trbk + '\n' + '{0}: {1}'.format(sys.exc_info()[0].__name__, sys.exc_info()[1])
        if content:
            content = '%s ' % content
        if Log._show_full_cls:
            class_name = Log.get_full_class_name()
        else:
            class_name = Log.get_simple_class_name()
        sys.stderr.write('{6}{0} {1} {2}/E {3}{4}{5}{7}\n'.format(
            Log.get_datetime_str(), class_name, Log.TAG, content, Log.get_file_info(), trbk,
            ConsoleColors.RED, ConsoleColors.END_CODE
        ))

    @classmethod
    def i(cls, content: object = None):
        if Log._level >= 0 and Log._level > Log.Level.INFO:
            return
        if content:
            content = '%s ' % content
        if Log._show_full_cls:
            class_name = Log.get_full_class_name()
        else:
            class_name = Log.get_simple_class_name()
        sys.stderr.write('{5}{0} {1} {2}/I {3}{4}{6}\n'.format(
            Log.get_datetime_str(), class_name, Log.TAG, content, Log.get_file_info(),
            ConsoleColors.WHITE, ConsoleColors.END_CODE
        ))

    @classmethod
    def v(cls, content: object = None):
        if Log._level >= 0 and Log._level > Log.Level.VERBOSE:
            return
        if content:
            content = '%s ' % content
        if Log._show_full_cls:
            class_name = Log.get_full_class_name()
        else:
            class_name = Log.get_simple_class_name()
        sys.stderr.write('{5}{0} {1} {2}/V {3}{4}{6}\n'.format(
            Log.get_datetime_str(), class_name, Log.TAG, content, Log.get_file_info(),
            ConsoleColors.WHITE, ConsoleColors.END_CODE
        ))

    @classmethod
    def d(cls, content: object = None):
        if Log._level >= 0 and Log._level > Log.Level.DEBUG:
            return
        if content:
            content = '%s ' % content
        if Log._show_full_cls:
            class_name = Log.get_full_class_name()
        else:
            class_name = Log.get_simple_class_name()
        sys.stderr.write('{5}{0} {1} {2}/D {3}{4}{6}\n'.format(
            Log.get_datetime_str(), class_name, Log.TAG, content, Log.get_file_info(),
            ConsoleColors.WHITE, ConsoleColors.END_CODE
        ))

    @classmethod
    def get_file_info(cls):
        caller_frame = inspect.stack()[2][0]
        return '({0}:{1:d})'.format(os.path.basename(caller_frame.f_code.co_filename), caller_frame.f_lineno)

    @classmethod
    def get_full_class_name(cls):
        caller_frame = inspect.stack()[2][0]
        class_name = '__main__.'
        if 'self' in caller_frame.f_locals:
            class_name = '%s.%s#' % (
                caller_frame.f_locals['self'].__class__.__module__, caller_frame.f_locals['self'].__class__.__name__
            )
        elif 'cls' in caller_frame.f_locals:
            class_name = '%s.%s.' % (
                caller_frame.f_locals['cls'].__module__, caller_frame.f_locals['cls'].__name__
            )
        return '{0}{1}'.format(class_name, caller_frame.f_code.co_name)

    @classmethod
    def get_simple_class_name(cls):
        caller_frame = inspect.stack()[2][0]
        class_name = '__main__.'
        if 'self' in caller_frame.f_locals:
            class_name = '%s#' % caller_frame.f_locals['self'].__class__.__name__
        elif 'cls' in caller_frame.f_locals:
            class_name = '%s.' % caller_frame.f_locals['cls'].__name__
        return '{0}{1}'.format(class_name, caller_frame.f_code.co_name)

    @classmethod
    def get_datetime_str(cls):
        now_time = datetime.datetime.now()
        return '{0}.{1:03.0f}'.format(now_time.strftime('%m-%d %H:%M:%S'), int(now_time.strftime('%f')) / 1000)
