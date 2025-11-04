from page.creditPlanPage import CreditPlans


def test_page_url(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - проверка, что действительно открыта страница "Планы и цены"
    assert plans_and_prices_page.check_current_url()

def test_credit_mode(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - переключение в режим кредитных пакетов"
    credit_plans_page = CreditPlans(driver)
    credit_plans_page.go_credit_plans_page()

    # Шаг 3 - проверка, что действительно выбран режим кредитных пакетов"
    assert credit_plans_page.check_selected_page()

def test_credit_plans(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - переключение в режим кредитных пакетов"
    credit_plans_page = CreditPlans(driver)
    credit_plans_page.go_credit_plans_page()

    # Шаг 3 - получение списка значений кредитных планов"
    lst_credit_plans = credit_plans_page.get_value_credit_plans()

    # Шаг 4 - проверка, что список кредитных планов непустой и текст соответствовал формату "число Кредит"/"число Кредита/ов" (пробелы и переносы обработаны)
    assert len(lst_credit_plans) > 0

    # Шаг 5 - проверка, что все значения кредитных планов больше нуля
    assert all(credit_plan > 0 for credit_plan in lst_credit_plans), f"Не все числа положительные: {lst_credit_plans}"

def test_prices(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - переключение в режим кредитных пакетов"
    credit_plans_page = CreditPlans(driver)
    credit_plans_page.go_credit_plans_page()

    # Шаг 3 - получение списка цен
    lst_prices = credit_plans_page.get_prices()

    # Шаг 4 - проверка, что список цен непустой, что изначальный элемент имел формат '$число USD месяц' (пробелы и переносы обработаны)
    assert len(lst_prices) > 0

    # Шаг 5 - проверка, что все цены больше нуля
    assert all(price > 0 for price in lst_prices), f"Не все числа положительные: {lst_prices}"

def test_discounts(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - переключение в режим кредитных пакетов"
    credit_plans_page = CreditPlans(driver)
    credit_plans_page.go_credit_plans_page()

    # Шаг 3 - получение списка скидок
    lst_discounts = credit_plans_page.get_discounts()

    # Шаг 4 - проверка, что скидки есть, что изначальный элемент имел формат 'Экономия $число**' (пробелы и переносы обработаны), добавены нули, как отсутствие скидки (требование)
    assert len(lst_discounts) > 2

    # Шаг 5 - проверка, что все скидки больше или равны нулю
    assert all(discount >= 0 for discount in lst_discounts), f"Не все числа положительные: {lst_discounts}"

def test_credit_buttons(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - переключение в режим кредитных пакетов"
    credit_plans_page = CreditPlans(driver)
    credit_plans_page.go_credit_plans_page()

    # Шаг 3 - получение списка значений кредитных планов"
    lst_credit_plans = credit_plans_page.get_value_credit_plans()

    # Шаг 4 - получение списка значений с кнопки Кпить кредит/ы
    lst_value_credit_button = credit_plans_page.get_value_credit_button(lst_credit_plans)

    # Шаг 5 - проверка, что значения с кнопки кредитов есть, что изначальный элемент имел формат 'Купить кредиты: число/Купить 1 кредит' (пробелы и переносы обработаны)
    assert len(lst_value_credit_button) > 0

    # Шаг 6 - проверка, что все значения с кнопки кредитов больше нуля
    assert all(value_credit_button > 0 for value_credit_button in lst_value_credit_button), f"Не все числа положительные: {lst_value_credit_button}"

def test_plans_buttons_match(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - переключение в режим кредитных пакетов"
    credit_plans_page = CreditPlans(driver)
    credit_plans_page.go_credit_plans_page()

    # Шаг 3 - получение списка значений кредитных планов"
    lst_credit_plans = credit_plans_page.get_value_credit_plans()

    # Шаг 4 - получение списка значений с кнопки Кпить кредит/ы
    lst_value_credit_button = credit_plans_page.get_value_credit_button(lst_credit_plans)

    # Шаг 5 - проверка, что списки кредитных планов и значений с кнопки кредитов полностью индентичны, при успехе проверять можно только один из них, возьмем "lst_credit_plans"
    assert lst_credit_plans == lst_value_credit_button

def test_lists_length(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - переключение в режим кредитных пакетов"
    credit_plans_page = CreditPlans(driver)
    credit_plans_page.go_credit_plans_page()

    # Шаг 3 - получение списка значений кредитных планов"
    lst_credit_plans = credit_plans_page.get_value_credit_plans()

    # Шаг 4 - получение списка цен
    lst_prices = credit_plans_page.get_prices()

    # Шаг 5 - получение списка скидок
    lst_discounts = credit_plans_page.get_discounts()

    # Шаг 6 - проверка, что списки имеют одинаковую длину
    assert credit_plans_page.compare_len_lst(lst_credit_plans, lst_prices, lst_discounts)

def test_progression(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - переключение в режим кредитных пакетов"
    credit_plans_page = CreditPlans(driver)
    credit_plans_page.go_credit_plans_page()

    # Шаг 3 - получение списка значений кредитных планов"
    lst_credit_plans = credit_plans_page.get_value_credit_plans()

    # Шаг 4 - получение списка цен
    lst_prices = credit_plans_page.get_prices()

    # Шаг 5 - получение списка скидок
    lst_discounts = credit_plans_page.get_discounts()

    # Шаг 6 - проверка, что логика прогрессии кредитных пакетов, цен и скидок не нарушены
    assert credit_plans_page.check_logic_credit_plans_prices_discounts(lst_credit_plans, lst_prices, lst_discounts)

def test_discount_price_ratio(authorized_user_on_plans_page):
    # Шаг 1 - авторизация и переход на страницу "Планы и цены"
    driver, plans_and_prices_page = authorized_user_on_plans_page

    # Шаг 2 - переключение в режим кредитных пакетов"
    credit_plans_page = CreditPlans(driver)
    credit_plans_page.go_credit_plans_page()

    # Шаг 3 - получение списка цен
    lst_prices = credit_plans_page.get_prices()

    # Шаг 4 - получение списка скидок
    lst_discounts = credit_plans_page.get_discounts()

    # Шаг 5 - проверка, что скидка меньше цены
    assert credit_plans_page.check_discount_less_than_price(lst_prices, lst_discounts)





# def test_credit_plans():
#     driver = initialization()
#     existing_emails = load_all_emails()
#     email = random.choice(existing_emails)
#     """Пункт 1 - авторизация пользователя"""
#     # Шаг 1.1 - открыть ресурс, перейти к странице авторизации
#     login_page = LoginPage(driver)
#     login_page.go_login_page()
#
#     # Шаг 1.2 - прохождение авторизации
#     login_page.enter_email(email)
#     login_page.enter_password(password)
#     login_page.login_click()
#
#     """Пункт 2 - выбор режима кредитных пакетов"""
#     #Шаг 2.1 - переход на страницу "Планы и цены"
#     plans_and_prices_page = PlansAndPrices(driver)
#     plans_and_prices_page.go_plans_and_prices_page()
#
#     # Шаг 2.2 - проверка, что действительно открыта страница "Планы и цены"
#     assert plans_and_prices_page.check_current_url()

    # # Шаг 2.3 - переключение в режим кредитных пакетов"
    # credit_plans_page = CreditPlans(driver)
    # credit_plans_page.go_credit_plans_page()
    #
    # # Шаг 2.4 - проверка, что действительно выбран режим кредитных пакетов"
    # assert credit_plans_page.check_selected_page()

    # """Пункт 3 - проверка корректности кредитных планов, цен и скидок"""
    #
    # # Шаг 3.1 - получение списка значений кредитных планов"
    # lst_credit_plans = credit_plans_page.get_value_credit_plans()
    #
    # # Шаг 3.2 - проверка, что список кредитных планов непустой и текст соответствовал формату "число Кредит"/"число Кредита/ов" (пробелы и переносы обработаны)
    # assert len(lst_credit_plans) > 0
    #
    # # Шаг 3.3 - проверка, что все значения кредитных планов больше нуля
    # assert all(credit_plan > 0 for credit_plan in lst_credit_plans), f"Не все числа положительные: {lst_credit_plans}"

    # # Шаг 3.4 - получение списка цен
    # lst_prices = credit_plans_page.get_prices()
    #
    # # Шаг 3.5 - проверка, что список цен непустой, что изначальный элемент имел формат '$число USD месяц' (пробелы и переносы обработаны)
    # assert len(lst_prices) > 0
    #
    # # Шаг 3.6 - проверка, что все цены больше нуля
    # assert all(price > 0 for price in lst_prices), f"Не все числа положительные: {lst_prices}"

    # # Шаг 3.7 - получение списка скидок
    # lst_discounts = credit_plans_page.get_discounts()
    #
    # # Шаг 3.8 - проверка, что скидки есть, что изначальный элемент имел формат 'Экономия $число**' (пробелы и переносы обработаны), добавлены нули, как отсутствие скидки (требование)
    # assert len(lst_discounts) > 2
    #
    # # Шаг 3.9 - проверка, что все скидки больше или равны нулю
    # assert all(discount >= 0 for discount in lst_discounts), f"Не все числа положительные: {lst_discounts}"

    # # Шаг 3.10 - получение списка значений с кнопки Кпить кредит/ы
    # lst_value_credit_button = credit_plans_page.get_value_credit_button(lst_credit_plans)
    #
    # # Шаг 3.11 - проверка, что значения с кнопки кредитов есть, что изначальный элемент имел формат 'Купить кредиты: число/Купить 1 кредит' (пробелы и переносы обработаны)
    # assert len(lst_value_credit_button) > 0
    #
    # # Шаг 3.12 - проверка, что все значения с кнопки кредитов больше нуля
    # assert all(value_credit_button > 0 for value_credit_button in lst_value_credit_button), f"Не все числа положительные: {lst_value_credit_button}"

    # # Шаг 3.13 - проверка, что списки кредитных планов и значений с кнопки кредитов полностью индентичны, при успехе проверять можно только один из них, возьмем "lst_credit_plans"
    # assert lst_credit_plans == lst_value_credit_button

    # # Шаг 3.14 - проверка, что списки имеют одинаковую длину
    # assert credit_plans_page.compare_len_lst(lst_credit_plans, lst_prices, lst_discounts)

    # # Шаг 3.15 - проверка, что логика прогрессии кредитных пакетов, цен и скидок не нарушены
    # assert credit_plans_page.check_logic_credit_plans_prices_discounts(lst_credit_plans, lst_prices, lst_discounts)

    # # Шаг 3.16 - проверка, что скидка меньше цены
    # assert credit_plans_page.check_discount_less_than_price(lst_prices, lst_discounts)




