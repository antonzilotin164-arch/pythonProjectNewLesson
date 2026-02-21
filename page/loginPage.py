from selenium.common import TimeoutException
from locators.locators import LocatorsLoginPage
from utilities.fileOperations import email_factory
from base.globalVariables import password
from base.initializationDriver import *


class LoginPage():
    def __init__(self, driver):
        self.driver = driver

    def go_login_page(self):
        button_entrance = wait_element(self.driver, LocatorsLoginPage.button_entrance_locator)
        button_entrance.click()

    def login(self, email=None):
        """Метод для авторизации. Если email не передан, генерируется новый"""
        if email is None:
            email = email_factory()

        # Переход на страницу логина
        self.go_login_page()

        # # Ввод почты
        # input_email = wait_element(self.driver, LocatorsLoginPage.email_locator)
        # input_email.send_keys(email)
        #
        # # Ввод пароля
        # input_password = wait_element(self.driver, LocatorsLoginPage.password_locator)
        # input_password.send_keys(password)
        #
        # # Нажатие кнопки войти
        # button_entrance = wait_element(self.driver, LocatorsLoginPage.entrance_locator)
        # button_entrance.click()


        # assert DriverInitialization.wait_element(self.driver, LocatorsLoginPage.button_accountIcon_locator)

        # Проверка на успешную авторизацию пользователя
        try:
            button_accountIcon = wait_element(self.driver, LocatorsLoginPage.button_accountIcon_locator)
            print(f"Пользователь {email} успешно авторизован")
            return True
        except TimeoutException:
            print("Сбой авторизации - пользователь не найден")
            return False

    def enter_email(self, email):
        # Ввод почты
        input_email = wait_element(self.driver, LocatorsLoginPage.email_locator, timeout=5)
        input_email.send_keys(email)

    def enter_password(self, password):
        # Ввод пароля
        input_password = wait_element(self.driver, LocatorsLoginPage.password_locator, timeout=5)
        input_password.send_keys(password)

    def login_click(self):
        # Нажатие кнопки войти
        button_entrance = wait_element(self.driver, LocatorsLoginPage.entrance_locator, timeout=5)
        button_entrance.click()




