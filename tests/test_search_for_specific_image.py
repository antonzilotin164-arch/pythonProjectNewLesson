import pytest
import random
from page.loginPage import LoginPage
from page.mainPage import MainPage
from page.registrationPage import RegistrationPage
from utilities.fileOperations import save_email, load_all_emails
from base.initializationDriver import *
from base.globalVariables import password, search_value, base_url

driver = initialization(base_url)
existing_emails = load_all_emails()
email = random.choice(existing_emails)


def test_search_for_specific_image():
    """Пункт 1 - авторизация пользователя"""
    #Шаг 1.1 - открыть ресурс, перейти к странице авторизации
    login_page = LoginPage(driver)
    login_page.go_login_page()

    #Шаг 1.2 - прохождение авторизации
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.login_click()

    """Пункт 2 - ввод запроса и поиск изображения"""
    #Шаг 2.1 - открытие поисковой строки
    main_page = MainPage(driver)
    main_page.click_search_field()

    #Шаг 2.2 - ввод значения в поисковую строку
    main_page.input_search_query()

    #Шаг 2.3 - проверка, что введенное значение совпадает с желаемым
    assert main_page.check_input_value(search_value)

    #Шаг 2.4 - проверка, что открылся список картинок
    assert main_page.check_list_query()

    #Шаг 2.5 - проверка, что список не пустой
    texts = main_page.get_list_query_texts()
    assert len(texts) > 0

    #Шаг 2.6 - проверка, что список поиска действительно имеет совпадение с поисковым значением
    assert main_page.check_value_elements(search_value, texts)
    print(texts)

    #Шаг 2.7 - поиск по заданному значению
    main_page.enter_to_search()

    #Шаг 2.8 - проверка, что мы находимся на корректной странице с картинками
    assert main_page.check_current_url()







