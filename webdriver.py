import os
import subprocess
import time

from abc import abstractmethod, ABC

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from .log import Log


# URLをダウンロードするためのライブラリ
class WebDriver(ABC):
    def __init__(self, exec_bin=None):
        Log.i("Starting WebDriver in selenium ...")
        self._driver = None
        self.initialize_driver(exec_bin)
        assert self._driver is not None, "WebDriver initialization failed."
        self._driver.implicitly_wait(10)  # seconds

    @abstractmethod
    def initialize_driver(self, exec_bin):
        raise NotImplementedError()

    @abstractmethod
    def restart_driver(self):
        raise NotImplementedError()

    def get_page_source(self, url):
        i = 0
        while i <= 10:
            if i == 5:
                Log.v('Restarting driver ...')
                self.restart_driver()
            try:
                self._driver.get(url)
            except TimeoutException:
                Log.w('from \'%s\', TimeoutException was raised, retrying #%d' % (url, i))
            else:
                return self._driver.page_source
            i += 1
            time.sleep(20)
        Log.e('Retrying failed')
        with open('error.log', 'a') as f:
            f.write('{0} E: TimeoutException was raised from url \'{1}\'\n'.format(Log.get_datetime_str(), url))
        return None

    def quit(self):
        self._driver.quit()


# URLをダウンロードするためのChrome用ライブラリ
class ChromeDriver(WebDriver):
    def __init__(self, exec_bin=None):
        super().__init__(exec_bin)
        self._chrome_options = None

    def restart_driver(self):
        self.quit()
        self._driver = webdriver.Chrome(chrome_options=self._chrome_options)

    def initialize_driver(self, exec_bin):
        options = Options()
        options.binary_location = None
        if exec_bin is None:
            if os.name == "posix":
                options.binary_location = subprocess.getoutput("which chrome")
            elif os.name == "nt":
                options.binary_location = subprocess.getoutput("where chrome")
        else:
            options.binary_location = exec_bin
        assert os.path.exists(options.binary_location), \
            "auto detection failed. Please specify chrome binary location"
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self._chrome_options = options
        self._driver = webdriver.Chrome(chrome_options=options)

    def close(self):
        self._driver.close()


# URLをダウンロードするためのFirefox用ライブラリ
class FirefoxDriver(WebDriver):
    def __init__(self, exec_bin=None):
        super().__init__(exec_bin)
        self._firefox_binary = None

    def restart_driver(self):
        self.quit()
        self._driver = webdriver.Firefox(firefox_binary=self._firefox_binary)

    def initialize_driver(self, exec_bin):
        if exec_bin is None:
            if os.name == "posix":
                exec_bin = subprocess.getoutput("which firefox")
            elif os.name == "nt":
                exec_bin = subprocess.getoutput("where firefox")
        assert exec_bin is not None and os.path.exists(exec_bin), \
            "auto detection failed. Please specify firefox binary location"
        binary = FirefoxBinary(exec_bin)
        binary.add_command_line_options('-headless')
        self._firefox_binary = binary
        self._driver = webdriver.Firefox(firefox_binary=binary)
