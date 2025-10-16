import pytest
import random
import unittest
from page.loginPage import LoginPage
from page.registrationPage import RegistrationPage
from utilities.fileOperations import load_all_emails
from base.globalVariables import password
from locators.locators import LocatorsRegistrationPage
from base.initializationDriver import *



driver = initialization()


@pytest.mark.order(2)
def test_duplicate_user_registration(duplicate_check_status):
    """Проверка системы на обнаружение дублирующихся пользователей"""

    login_page = LoginPage(driver)
    registration_page = RegistrationPage(driver)

    # Переход на страницу регистрации
    login_page.go_login_page()
    registration_page.go_registration_page()

    # Получение и проверка существующих email
    existing_emails = load_all_emails()
    print(existing_emails)
    assert existing_emails, "Нет существующих email для тестирования"

    # Выбор существующего email
    email = random.choice(existing_emails)
    print(f"Тестируем регистрацию с существующим email: {email}")

    # Процесс регистрации
    registration_page.enter_email(email)
    registration_page.enter_password(password)
    registration_page.enter_password_confirm(password)
    registration_page.registration_click()

    # Проверка, что система обнаружила дублирующегося пользователя
    user_exists = registration_page.check_user_not_existing()

    assert not user_exists
