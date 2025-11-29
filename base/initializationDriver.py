from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import unittest
import urllib.parse
import time
from pathlib import Path


def initialization(url, download_dir=None, return_tuple=False):
    # Инициализация опций для Chrome
    options = webdriver.ChromeOptions()

    # Базовые опции
    options.add_argument("--incognito")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument('ignore-certificate-errors')

    # НАСТРОЙКИ СКАЧИВАНИЯ - ТАК РАБОТАЕТ
    if download_dir is None:
        download_dir = Path(__file__).parent.parent / "downloads"

    # Создаем папку если не существует
    download_dir.mkdir(parents=True, exist_ok=True)

    prefs = {
        "download.default_directory": str(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,  # ОТКЛЮЧАЕМ безопасный просмотр
        "profile.default_content_settings.popups": 0,
    }
    options.add_experimental_option("prefs", prefs)

    # Отключаем автоматизационные флаги
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Инициализация драйвера
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

    # Убираем webdriver флаг
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(url)

    if return_tuple:
        return driver, download_dir
    else:
        return driver


def stop_driver(driver):
    driver.close()
    driver.quit()


class Steps(unittest.TestCase):
    def get_address(self, driver, address):
        try:
            driver.get(address)
            pass
        except TimeoutException:
            stop_driver(driver)
            self.fail("Exception while trying to connect to " + address)


@staticmethod
def wait_element(driver, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


@staticmethod
def wait_url(driver, timeout=10):
    WebDriverWait(driver, timeout).until(lambda d: d.current_url)
    return driver.current_url


@staticmethod
def wait_elements(driver, locator, timeout=30):
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located(locator)
    )
    time.sleep(1)
    return elements


@staticmethod
def check_current_url(driver, basis_current_url, add_value_url):
    wait_url(driver, timeout=10)
    get_current_url = driver.current_url
    encoded_add_value_url = urllib.parse.quote(add_value_url)
    factory_current_url = basis_current_url + encoded_add_value_url
    if get_current_url == factory_current_url:
        return True
    else:
        return False