import codecs
import json
import os
import subprocess
import tempfile
import time

from abc import abstractmethod, ABC

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities

from .log import Log
# from .pdfdriver import PDFDriver


# URLをダウンロードするためのライブラリ
class WebDriver(ABC):
    def __init__(self, exec_bin=None):
        Log.i("Starting WebDriver in selenium ...")
        self._driver = None
        self._temp_dir_path = tempfile.TemporaryDirectory("_" + self.__class__.__name__).name
        self.initialize_driver(exec_bin)
        assert self._driver is not None, "WebDriver initialization failed."
        self._driver.implicitly_wait(10)  # seconds

    @abstractmethod
    def initialize_driver(self, exec_bin):
        raise NotImplementedError()

    @abstractmethod
    def get_status_code(self) -> int:
        raise NotImplementedError()

    def get_temp_dir(self):
        return self._temp_dir_path

    def get_page_source(self, url):
        if not url:
            return None
        i = 0
        while i <= 10:
            try:
                self._driver.get(url)
                if self.get_status_code() != 200:
                    with codecs.open('error.log', 'a', 'utf_8') as f:
                        f.write('{0} E: Status code was not 200 from url \'{1}\'\n'.format(
                            Log.get_datetime_str(), url
                        ))
                    return None
            except TimeoutException:
                Log.w('from \'%s\', TimeoutException was raised, retrying #%d' % (url, i))
            else:
                # if re.search('\.pdf(?:\?.*)?$', url, re.IGNORECASE):
                #     return WebDriver.wrap_content_tag(PDFDriver.get_content(url))
                # else:
                return self._driver.page_source
            i += 1
            time.sleep(20)
        Log.e('Retrying failed')
        with codecs.open('error.log', 'a', 'utf_8') as f:
            f.write('{0} E: TimeoutException was raised from url \'{1}\'\n'.format(Log.get_datetime_str(), url))
        return None

    def quit(self):
        self._driver.quit()


# URLをダウンロードするためのChrome用ライブラリ
class ChromeDriver(WebDriver):
    def get_status_code(self) -> int:
        perf_log = self._driver.get_log('performance')
        for i in range(len(perf_log) - 1, 0, -1):
            log = json.loads(perf_log[i]['message'])
            if log['message']['method'] == 'Network.responseReceived':
                return int(log['message']['params']['response']['status'])

    def initialize_driver(self, exec_bin):
        options = webdriver.ChromeOptions()
        options.binary_location = exec_bin

        if exec_bin is None:
            if os.name == "posix":
                options.binary_location = subprocess.getoutput("which chrome")
            elif os.name == "nt":
                options.binary_location = subprocess.getoutput("where chrome")

        assert os.path.exists(options.binary_location), \
            "auto detection failed. Please specify chrome binary location"

        options.add_experimental_option("prefs", {
            "download.default_directory": self.get_temp_dir(),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.plugins_disabled": ["Chrome PDF Viewer"],
            "plugins.always_open_pdf_externally": True
        })
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-print-preview")

        cap = DesiredCapabilities.CHROME
        cap['loggingPrefs'] = {'performance': 'ALL'}
        self._driver = webdriver.Chrome(chrome_options=options, desired_capabilities=cap)


# URLをダウンロードするためのFirefox用ライブラリ
class FirefoxDriver(WebDriver):
    def get_status_code(self) -> int:
        return 200
        # TODO: Status code cannot retrieve
        # perf_log = self._driver.get_log('info')
        # for i in range(len(perf_log) - 1, 0, -1):
        #     log = json.loads(perf_log[i]['message'])
        #     print(json.dumps(log, indent=4))
        #     if log['message']['method'] == 'Network.responseReceived':
        #         return int(log['message']['params']['response']['status'])

    def initialize_driver(self, exec_bin):
        options = webdriver.FirefoxOptions()
        options.binary_location = exec_bin

        if exec_bin is None:
            if os.name == "posix":
                options.binary_location = subprocess.getoutput("which firefox")
            elif os.name == "nt":
                options.binary_location = subprocess.getoutput("where firefox")

        assert os.path.exists(options.binary_location), \
            "auto detection failed. Please specify firefox binary location"

        options.add_argument('-headless')

        options.log.level = 'trace'
        cap = DesiredCapabilities.FIREFOX
        cap["marionette"] = True
        cap['acceptSslCerts'] = True
        self._driver = webdriver.Firefox(firefox_options=options, desired_capabilities=cap)
