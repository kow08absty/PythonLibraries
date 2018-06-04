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
    def _line_end(cls, kwargs: dict = ()):
        if 'end' in kwargs.keys():
            sys.stderr.write(kwargs['end'])
        else:
            sys.stderr.write('\n')

    @classmethod
    def _print(cls, level_symbol='', contents=()):
        trbk = ''.join(traceback.format_tb(sys.exc_info()[2])).strip()
        if trbk:
            trbk = '\n' + trbk + '\n' + '{0}: {1}'.format(sys.exc_info()[0].__name__, sys.exc_info()[1])
        if len(contents) > 1:
            contents = '%s ' % (contents,)
        elif len(contents) == 1:
            contents = '%s ' % (contents[0], )
        else:
            contents = ''
        if cls._show_full_cls:
            class_name = cls.get_full_class_name()
        else:
            class_name = cls.get_simple_class_name()
            if level_symbol:
                level_symbol = '/' + level_symbol
        sys.stderr.write('{0} {1} {2}/{6} {3}{4}{5}'.format(
            cls.get_datetime_str(), class_name, cls.TAG, contents, cls.get_file_info(), trbk, level_symbol
        ))

    @classmethod
    def set_level(cls, level):
        cls._level = level

    @classmethod
    def set_show_full_class_name(cls, b: bool = False):
        cls._show_full_cls = b

    @classmethod
    def w(cls, *contents, **kwargs):
        if cls._level >= 0 and cls._level > Log.Level.WARN:
            return
        sys.stderr.write(ConsoleColors.YELLOW)
        cls._print('W', contents)
        sys.stderr.write(ConsoleColors.END_CODE)
        cls._line_end(kwargs)

    @classmethod
    def e(cls, *contents, **kwargs):
        if cls._level >= 0 and cls._level > Log.Level.ERROR:
            return
        sys.stderr.write(ConsoleColors.RED)
        cls._print('E', contents)
        sys.stderr.write(ConsoleColors.END_CODE)
        cls._line_end(kwargs)

    @classmethod
    def i(cls, *contents, **kwargs):
        if cls._level >= 0 and cls._level > Log.Level.INFO:
            return
        cls._print('D', contents)
        cls._line_end(kwargs)

    @classmethod
    def v(cls, *contents, **kwargs):
        if cls._level >= 0 and cls._level > Log.Level.VERBOSE:
            return
        cls._print('D', contents)
        cls._line_end(kwargs)

    @classmethod
    def d(cls, *contents, **kwargs):
        if cls._level >= 0 and cls._level > Log.Level.DEBUG:
            return
        cls._print('D', contents)
        cls._line_end(kwargs)

    @classmethod
    def get_file_info(cls):
        caller_frame = inspect.stack()[3][0]
        return '({0}:{1:d})'.format(os.path.basename(caller_frame.f_code.co_filename), caller_frame.f_lineno)

    @classmethod
    def get_full_class_name(cls):
        caller_frame = inspect.stack()[3][0]
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
        caller_frame = inspect.stack()[3][0]
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
