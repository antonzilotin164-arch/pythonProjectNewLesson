from selenium.common import TimeoutException
from locators.locators import LocatorsLoginPage
from base.initializationDriver import DriverInitialization
from utilities.fileOperations import email_factory
from base.globalVariables import password


class LoginPage():
    def __init__(self, driver):
        self.driver = driver

    def go_login_page(self):
        button_entrance = DriverInitialization.wait_element(self.driver, LocatorsLoginPage.button_entrance_locator)
        button_entrance.click()

    def login(self, email=None):
        """Метод для авторизации. Если email не передан, генерируется новый"""
        if email is None:
            email = email_factory()

        # Переход на страницу логина
        self.go_login_page()

        # Ввод почты
        input_email = DriverInitialization.wait_element(self.driver, LocatorsLoginPage.email_locator)
        input_email.send_keys(email)

        # Ввод пароля
        input_password = DriverInitialization.wait_element(self.driver, LocatorsLoginPage.password_locator)
        input_password.send_keys(password)

        # Нажатие кнопки войти
        button_entrance = DriverInitialization.wait_element(self.driver, LocatorsLoginPage.entrance_locator)
        button_entrance.click()

        # Проверка на успешную авторизацию пользователя
        try:
            button_accountIcon = DriverInitialization.wait_element(self.driver, LocatorsLoginPage.button_accountIcon_locator)
            print(f"Пользователь {email} успешно авторизован")
            return True
        except TimeoutException:
            print("Сбой авторизации - пользователь не найден")
            return False






