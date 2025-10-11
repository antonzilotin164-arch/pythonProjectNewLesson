import pytest

from page.loginPage import LoginPage
from page.registrationPage import RegistrationPage
from utilities.fileOperations import save_email
from base.initializationDriver import *

driver = initialization()

@pytest.mark.order(2)
def test_registration():
    login_page = LoginPage(driver)
    registration_page = RegistrationPage(driver)
    login_page.go_login_page()
    registration_page.go_registration_page()
    assert registration_page.start_registration()
    assert not registration_page.check_existing_user_error()

    # 1. Пользователь заходит на главную страницу
    # 2. Пользователь кликает на кнопку "Авторизация"
    # 3. Пользователь выбирает вариант регистрации
    # 4. Пользователь вводит логин
    # ......