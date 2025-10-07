from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from base.globalVariables import base_url
from selenium.webdriver.support import expected_conditions as EC

class DriverInitialization():
    def initialization(self):
        # Инициализация опций для Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")  # Запуск в режиме инкогнито
        options.add_experimental_option("detach", True)  # Оставить браузер открытым после завершения скрипта

        # Инициализация драйвера с опциями
        driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        # Вход на сайт
        # base_url = 'https://www.saucedemo.com/'
        driver.get(base_url)
        driver.maximize_window()

        return driver

    @staticmethod
    def wait_element(driver, locator, timeout=30):
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

