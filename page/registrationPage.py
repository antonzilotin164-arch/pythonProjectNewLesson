from selenium.common import TimeoutException
from locators.locators import LocatorsRegistrationPage
from utilities.fileOperations import email_factory, save_email
from utilities.validation import validate_email
from base.globalVariables import password
from base.initializationDriver import *


class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.used_email = None  # Для хранения email, использованного при регистрации

    def go_registration_page(self):
        button_create = wait_element(self.driver, LocatorsRegistrationPage.button_create_locator)
        button_create.click()

    def start_registration(self):
        # Процесс получения/создания почты
        email = email_factory()
        if not email:
            print("Ошибка генерации email")
            return None

        self.used_email = email  # Сохраняем email для последующего использования

        # Ввод данных пользователя
        if not validate_email(email):
            print("Ошибка валидации")
            return None

        return email

    def enter_email(self, email):
        # Ввод email
        button_email = wait_element(self.driver, LocatorsRegistrationPage.button_email_locator)
        button_email.send_keys(email)

    def enter_password(self, password):
        # Ввод пароля
        button_password = wait_element(self.driver, LocatorsRegistrationPage.button_password_locator)
        button_password.send_keys(password)

    def enter_password_confirm(self, confirmation):
        # Подтверждение пароля
        button_confirmation = wait_element(self.driver, LocatorsRegistrationPage.button_confirmation_locator)
        button_confirmation.send_keys(confirmation)

    def registration_click(self):
        # Нажатие кнопки регистрации
        button_regist = wait_element(self.driver, LocatorsRegistrationPage.button_regist_locator)
        button_regist.click()

    def check_user_not_existing(self):

        try:
            wait_element(self.driver, LocatorsRegistrationPage.error_existing, timeout=5)
            return False
        except TimeoutException:
            return True

    def check_password_match(self):

        try:
            wait_element(self.driver, LocatorsRegistrationPage.error_confirmation_not_match, timeout=5)
            return True
        except TimeoutException:
            return False

    def check_registration_success(self):
        """Проверка успешной регистрации"""
        try:
            button_accountIcon = wait_element(self.driver, LocatorsRegistrationPage.button_accountIcon_locator, timeout=10)
            print("Регистрация успешна!")
            print(f"Пользователь {self.used_email} зарегистрирован!")
            return True
        except TimeoutException:
            print("Сбой регистрации - элемент не найден")
            return False








