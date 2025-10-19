import random
from page.loginPage import LoginPage
from page.plansAndPrices import PlansAndPrices
from utilities.fileOperations import load_all_emails
from base.initializationDriver import *
from base.globalVariables import password

driver = initialization()
existing_emails = load_all_emails()
email = random.choice(existing_emails)

def test_plans_and_prices_page_display():
    """Пункт 1 - авторизация пользователя"""
    # Шаг 1.1 - открыть ресурс, перейти к странице авторизации
    login_page = LoginPage(driver)
    login_page.go_login_page()

    # Шаг 1.2 - прохождение авторизации
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.login_click()
    """Пункт 2 - переход на страницу Планы и цены"""
    #Шаг 2.1 - переход на страницу "Планы и цены"
    plans_and_prices_page = PlansAndPrices(driver)
    plans_and_prices_page.go_plans_and_prices_page()

    # Шаг 2.2 - проверка, что действительно открыта страница "Планы и цены"
    assert plans_and_prices_page.check_current_url()

    """Пункт 3 - проверка первого блока на корректность отображения планов и цен"""

    # Шаг 3.1 - проверка, что выбран режим подписок
    assert plans_and_prices_page.check_subscription_mode_selected()

    # Шаг 3.2 - проверка, что выбран режим годовой подписки
    assert plans_and_prices_page.check_annual_tariff_active()

    # Шаг 3.4 - получение годовых пакетов плана
    pack_plans_annual = plans_and_prices_page.get_download_caps_numbers()

    #Шаг 3.5 - проверка, что список годовых пакетов использования непустой
    assert len(pack_plans_annual) > 0

    # Шаг 3.6 - проверка, что все значения годовых пакетов больше нуля
    assert all(num > 0 for num in pack_plans_annual), f"Не все числа положительные: {pack_plans_annual}"

    # Шаг 3.7 - получение списка цен годовых пакетов
    lst_price_annual = plans_and_prices_page.get_prices(pack_plans_annual)

    # Шаг 3.8 - проверка, что список цен годовых пакетов непустой, что изначальный элемент имел формат '$число USD месяц' (пробелы и переносы обработаны)
    assert len(lst_price_annual) > 0

    # Шаг 3.9 - проверка, что все годовые цены больше нуля
    assert all(num > 0 for num in lst_price_annual), f"Не все числа положительные: {lst_price_annual}"

    # Шаг 3.10 - проверка, что логика прогрессии годовых цен и пакетов не нарушена
    assert plans_and_prices_page.check_logic_pack_and_prices(pack_plans_annual, lst_price_annual)

    # Шаг 3.11 - получение списка годовых цен за загрузку
    prices_per_download_annual = plans_and_prices_page.get_prices_per_download(pack_plans_annual)

    # Шаг 3.12 - проверка, что список годовых цен за загрузку непустой, что изначальный элемент имел формат '$число за загрузку' (пробелы и переносы обработаны)
    assert len(prices_per_download_annual) > 0

    # Шаг 3.13 - проверка, что все годовые цены за загрузку больше нуля
    assert all(num > 0 for num in prices_per_download_annual), f"Не все числа положительные: {prices_per_download_annual}"

    # Шаг 3.14 - проверка, что все годовые цены за загрузку меньше или равны предыдущему (требование)
    assert plans_and_prices_page.check_logic_prices_per_download(prices_per_download_annual)

    """Пункт 4 - проверка второго блока на корректность отображения планов и цен"""

    # Шаг 4.1 - переход на месячный тариф
    plans_and_prices_page.go_month_tariff()

    # Шаг 4.2 - проверка, что выбран помесячный режим подписки
    assert plans_and_prices_page.check_month_tariff_active()

    # Шаг 4.3 - получение помесячных пакетов плана
    pack_plans_month = plans_and_prices_page.get_download_caps_numbers()

    # Шаг 4.4 - проверка, что список помесячных пакетов использования непустой
    assert len(pack_plans_month) > 0

    # Шаг 4.5 - проверка, что все значения помесячных пакетов больше нуля
    assert all(num > 0 for num in pack_plans_month), f"Не все числа положительные: {pack_plans_month}"

    # Шаг 4.6 - получение списка цен помесячных пакетов
    lst_price_month = plans_and_prices_page.get_prices(pack_plans_month)

    # Шаг 4.7 - проверка, что список цен помесячных пакетов непустой, что изначальный элемент имел формат '$число USD месяц' (пробелы и переносы обработаны)
    assert len(lst_price_month) > 0

    # Шаг 4.8 - проверка, что все помесячные цены больше нуля
    assert all(num > 0 for num in lst_price_month), f"Не все числа положительные: {lst_price_month}"

    # Шаг 4.9 - проверка, что логика прогрессии помесячных цен и пакетов не нарушена
    assert plans_and_prices_page.check_logic_pack_and_prices(pack_plans_month, lst_price_month)

    # Шаг 4.10 - получение списка помесячных цен за загрузку
    prices_per_download_month = plans_and_prices_page.get_prices_per_download(pack_plans_month)

    # Шаг 4.11 - проверка, что список помесячных цен за загрузку непустой, что изначальный элемент имел формат '$число за загрузку' (пробелы и переносы обработаны)
    assert len(prices_per_download_month) > 0

    # Шаг 4.12 - проверка, что все помесячные цены за загрузку больше нуля
    assert all(num > 0 for num in prices_per_download_month), f"Не все числа положительные: {prices_per_download_month}"

    # Шаг 4.13 - проверка, что все помесячные цены за загрузку меньше или равны предыдущему (требование)
    assert plans_and_prices_page.check_logic_prices_per_download(prices_per_download_month)

    """Пункт 5 - проверка, что годовые и помесячные цены корректны относительно друг друга"""

    # Шаг 5.1 - проверка, что число кредитов в пакетах совпадают (требование)
    assert pack_plans_annual == pack_plans_month

    # Шаг 5.12 - проверка, что цены пакетов за месяц больше или равны ценам за год
    assert plans_and_prices_page.comparison_lst_price(lst_price_month, lst_price_annual)

    # # Шаг 5.13 - проверка, что цены пакетов за одну загрузку за месяц больше или равны ценам за год
    assert plans_and_prices_page.comparison_lst_price_per_download(prices_per_download_month, prices_per_download_annual)







