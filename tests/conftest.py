import random
import pytest
from base.initializationDriver import initialization, stop_driver
from utilities.fileOperations import load_all_emails
from page.loginPage import LoginPage
from base.globalVariables import password
from page.plansAndPrices import PlansAndPrices

@pytest.fixture()
def setup(request):
    request.cls.driver = initialization
    #request.cls.screenshot(request.cls)
    yield
    stop_driver(request.cls.driver)

@pytest.fixture(scope="function")
def authenticated_user():
    """Фикстура для авторизации пользователя перед тестом"""
    driver = initialization()
    existing_emails = load_all_emails()
    email = random.choice(existing_emails)

    # Шаг 1.1 - открыть ресурс, перейти к странице авторизации
    login_page = LoginPage(driver)
    login_page.go_login_page()

    # Шаг 1.2 - прохождение авторизации
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.login_click()

    yield driver

    # Пост-условие - закрытие браузера
    driver.quit()

@pytest.fixture(scope="function")
def authorized_user_on_plans_page():
    """Фикстура для авторизованного пользователя на странице планов и цен"""
    driver = initialization()
    existing_emails = load_all_emails()
    email = random.choice(existing_emails)

    # Шаг 1 - открыть ресурс, перейти к странице авторизации
    login_page = LoginPage(driver)
    login_page.go_login_page()

    # Шаг 2 - прохождение авторизации
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.login_click()

    # Шаг 3 - переход на страницу "Планы и цены"
    plans_and_prices_page = PlansAndPrices(driver)
    plans_and_prices_page.go_plans_and_prices_page()

    yield driver, plans_and_prices_page  # Возвращаем и driver и объект страницы

    # Пост-условие - закрытие браузера
    driver.quit()