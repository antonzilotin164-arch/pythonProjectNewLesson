from selenium.common import TimeoutException
from base.initializationDriver import DriverInitialization
from locators.locators import LocatorsRegistrationPage
from utilities.fileOperations import email_factory, save_email
from utilities.validation import validate_email
from base.globalVariables import password

class RegistrationPage():
    def __init__(self, driver):
        self.driver = driver
        self.used_email = None  # Для хранения email, использованного при регистрации

    def go_registration_page(self):
        button_create = DriverInitialization.wait_element(self.driver, LocatorsRegistrationPage.button_create_locator)
        button_create.click()

    def start_registration(self):
        # Процесс получения/создания почты
        email = email_factory()
        if not email:
            print("Ошибка генерации email")
            return False

        self.used_email = email  # Сохраняем email для последующего использования

        # Ввод данных пользователя
        if not validate_email(email):
            print("Ошибка валидации")
            return False

        # Ввод email
        button_email = DriverInitialization.wait_element(self.driver, LocatorsRegistrationPage.button_email_locator)
        button_email.send_keys(email)

        # Ввод пароля
        button_password = DriverInitialization.wait_element(self.driver, LocatorsRegistrationPage.button_password_locator)
        button_password.send_keys(password)

        # Подтверждение пароля
        button_confirmation = DriverInitialization.wait_element(self.driver, LocatorsRegistrationPage.button_confirmation_locator)
        button_confirmation.send_keys(password)

        # Нажатие кнопки регистрации
        button_regist = DriverInitialization.wait_element(self.driver, LocatorsRegistrationPage.button_regist_locator)
        button_regist.click()

        return True

    def check_existing_user_error(self):
        """Проверка на сообщение о существующем пользователе"""
        try:
            error_message = DriverInitialization.wait_element(self.driver, LocatorsRegistrationPage.error_locator, timeout=5)
            print("Пользователь уже существует!")
            return True
        except TimeoutException:
            return False

    def check_registration_success(self):
        """Проверка успешной регистрации"""
        try:
            button_accountIcon = DriverInitialization.wait_element(self.driver, LocatorsRegistrationPage.button_accountIcon_locator, timeout=10)
            print("Регистрация успешна!")
            print(f"Пользователь {self.used_email} зарегистрирован!")
            return True
        except TimeoutException:
            print("Сбой регистрации - элемент не найден")
            return False








