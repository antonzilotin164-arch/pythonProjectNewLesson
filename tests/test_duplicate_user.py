import pytest
import random
from base.initializationDriver import DriverInitialization
from page.loginPage import LoginPage
from page.registrationPage import RegistrationPage
from utilities.fileOperations import load_all_emails
from base.globalVariables import password
from locators.locators import LocatorsRegistrationPage


@pytest.mark.order(1)
def test_duplicate_user_registration(duplicate_check_status):
    """Проверка системы на обнаружение дублирующихся пользователей"""

    start_page = DriverInitialization()
    driver = start_page.initialization()
    login_page = LoginPage(driver)
    registration_page = RegistrationPage(driver)

    try:
        existing_emails = load_all_emails()
        if not existing_emails:
            print("Нет существующих email для тестирования")
            pytest.fail("Нет существующих email для тестирования")

        email = random.choice(existing_emails)
        print(f"Тестируем регистрацию с существующим email: {email}")

        login_page.go_login_page()
        registration_page.go_registration_page()

        button_email = DriverInitialization.wait_element(driver, LocatorsRegistrationPage.button_email_locator)
        button_email.send_keys(email)

        button_password = DriverInitialization.wait_element(driver, LocatorsRegistrationPage.button_password_locator)
        button_password.send_keys(password)

        button_confirmation = DriverInitialization.wait_element(driver, LocatorsRegistrationPage.button_confirmation_locator)
        button_confirmation.send_keys(password)

        button_regist = DriverInitialization.wait_element(driver, LocatorsRegistrationPage.button_regist_locator)
        button_regist.click()

        user_exists = registration_page.check_existing_user_error()

        if user_exists:
            print("Пользователь уже существует, система исправна")
            duplicate_check_status["passed"] = True  #Важно: обновляем статус
        else:
            print("Сообщения о существующем пользователе нет, система неисправна")
            pytest.fail("Система неисправна - не обнаружено дублирование пользователя")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        pytest.fail(f"Произошла ошибка: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass