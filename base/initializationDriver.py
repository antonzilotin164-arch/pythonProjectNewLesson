from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from base.globalVariables import base_url
from selenium.webdriver.support import expected_conditions as EC
import unittest


def initialization():
    # Инициализация опций для Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")  # Запуск в режиме инкогнито

    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument('ignore-certificate-errors')

    # options.add_experimental_option("detach", True)  # Оставить браузер открытым после завершения скрипта

    # Инициализация драйвера с опциями
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    driver.get(base_url)
    # driver.maximize_window()

    return driver


def stop_driver(self):
    self.close()
    self.quit()


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
    # Гарантированно ждем 1 секунду
    WebDriverWait(driver, 1).until(lambda x: True)
    return elements
