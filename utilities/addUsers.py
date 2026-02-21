from selenium.common import TimeoutException

from locators.locators import LocatorsAddUser
from page.loginPage import LoginPage
from utilities.fileOperations import email_factory, save_email


class AddUser():

    def __init__(self, driver):  # Принимаем драйвер
        self.driver = driver  # Сохраняем драйвер

    def check_presence_registration(self):
        # Проверка на исключение регистрации существующего пользователя
        try:
            # Ищем сообщение о существующем пользователе
            error_message = self.driver.wait_element(self.driver, LocatorsAddUser.error_locator)
            print("Пользователь уже существует!")
            self.driver.quit()

            # Пытаемся авторизоваться
            login_page = LoginPage(self.driver)
            if login_page.login():
                email = email_factory()
                save_email(email)
                return True
            else:
                print("Ошибка авторизации существующего пользователя")
                return False

        except TimeoutException:
            print("Сообщения о существующем пользователе нет - продолжаем регистрацию")
