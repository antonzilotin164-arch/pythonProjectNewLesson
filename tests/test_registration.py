import pytest
from base.initializationDriver import DriverInitialization
from page.loginPage import LoginPage
from page.registrationPage import RegistrationPage
from utilities.fileOperations import save_email


@pytest.mark.order(2)
def test_registration(duplicate_check_status):
    """
    Тест регистрации нового пользователя.
    Запускается, только если test_duplicate_user_registration прошел успешно.
    """
    # Проверяем статус первого теста в начале функции
    if not duplicate_check_status["passed"]:
        pytest.fail("Система неисправна! Первый тест не пройден, нет смысла запускать регистрацию")

    start_page = DriverInitialization()
    driver = start_page.initialization()
    login_page = LoginPage(driver)
    registration_page = RegistrationPage(driver)

    try:
        login_page.go_login_page()
        registration_page.go_registration_page()

        registration_success = registration_page.start_registration()

        if registration_success:
            user_exists = registration_page.check_existing_user_error()

            if user_exists:
                print("Обнаружен существующий пользователь, пробуем авторизоваться...")
                driver.quit()

                new_driver = DriverInitialization().initialization()
                auth_login_page = LoginPage(new_driver)

                if auth_login_page.login(registration_page.used_email):
                    save_email(registration_page.used_email)
                    print("Успешная авторизация под существующим пользователем")
                    new_driver.quit()
                else:
                    print("Ошибка авторизации существующего пользователя")
                    new_driver.quit()
                    pytest.fail("Не удалось авторизоваться под существующим пользователем")
            else:
                if registration_page.check_registration_success():
                    save_email(registration_page.used_email)
                    print("Новый пользователь успешно зарегистрирован")
                else:
                    print("Регистрация не удалась")
                    pytest.fail("Регистрация нового пользователя не удалась")
        else:
            print("Ошибка в процессе регистрации")
            pytest.fail("Ошибка в процессе регистрации")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        pytest.fail(f"Произошла ошибка: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

