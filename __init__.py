# from .<fileName> import <className>
from .log import Log, ConsoleColors
from .webdriver import FirefoxDriver, ChromeDriver, WebDriver
from .sqlite3 import SQLite3
from .mimetypes import MimeTypes, _MimeEntryReflection as MimeEntry
from .pdfutil import PDFUtil
from .curldownloader import CurlDownloader
from .file import FileUtil


def contains_in_list(_l: list, _filter: callable) -> bool:
    for x in _l:
        if _filter(x):
            return True
    return False
