import re
import time

from locators.locators import LocatorsPlansAndPrisesPage, LocatorsLoginPage
from base.globalVariables import add_value_url_for_plans_and_prices, basis_current_url_for_page_plans_and_prises
from base.initializationDriver import *
from base.flagActivePage import FlagActivePage

class PlansAndPrices():
    def __init__(self, driver):
        self.driver = driver

    def go_plans_and_prices_page(self):
        button_plans_and_prices = wait_element(self.driver, LocatorsLoginPage.plans_and_prises, timeout=10)
        button_plans_and_prices.click()

    def check_current_url(self):
        result = check_current_url(self.driver, basis_current_url_for_page_plans_and_prises, add_value_url_for_plans_and_prices)
        if result:
            print("Текущий этап выполнен, мы на странице \"Планы и цены\"")
            return result
        else:
            print("Сбой, мы не попали на страницу \"Планы и цены\"")
            return result

    def check_subscription_mode_selected(self):
        button_subscribe = wait_element(self.driver, LocatorsPlansAndPrisesPage.button_subscribe, timeout=10)
        active_flag = wait_element(self.driver, LocatorsPlansAndPrisesPage.active_flag, timeout=10)
        if button_subscribe and active_flag:
            print("Выбран режим по умолчанию - Подписки. Это соответсвует требованиям")
            return True
        else:
            print("Выбран режим по умолчанию - Кредитов. Это не соответсвует требованиям")
            return False

    def check_annual_tariff_active(self):
        try:
            # Находим элемент
            element = wait_element(self.driver, LocatorsPlansAndPrisesPage.annual_tariff, timeout=10)

            # Получаем его классы
            classes = element.get_attribute("class")

            # Проверяем есть ли там магический класс
            if FlagActivePage.flag_check_active_tariff in classes:
                print("Выбран режим годового тарифа, это соответствует требованиям")
                return True
            else:
                print("Выбран другой режим, это не соответствие требованиям")
                return False

        except:
            print("Элемент не найден")
            return False

    def get_download_caps_numbers(self):
        buttons = wait_elements(self.driver, LocatorsPlansAndPrisesPage.download_caps, timeout=10)
        print(f"Найдено кнопок: {len(buttons)}")
        pack_plans = []
        for button in buttons:
            text = button.text.strip()
            print(f"Текст кнопки: '{text}'")
            # Разделяем текст любыми способами
            found_numbers = re.findall(r'\d+', text)
            # Ищем все числа в тексте
            pack_plans.extend([int(num) for num in found_numbers])

        print(f"Полученные значения пакетов: {pack_plans}")
        return pack_plans

    def get_prices(self, pack_plans):
        lst_prices = []

        for i in range(len(pack_plans)):
            one_pack = wait_element(self.driver, LocatorsPlansAndPrisesPage.get_pack_credit_locator(pack_plans[i]), timeout=10)

            if one_pack:
                one_pack.click()
                one_price = wait_element(self.driver, LocatorsPlansAndPrisesPage.one_price, timeout=10)

                if not one_price:
                    raise Exception(f"Не найден элемент с ценой после клика на кнопку с числом {pack_plans[i]}")

                price_text = one_price.text.strip()
                print(f"Текст элемента: '{price_text}'")

                # Проверяем несколько возможных форматов
                price_match = re.search(r'\$(\d+)', price_text)  # $15
                if not price_match:
                    price_match = re.search(r'(\d+)\s*USD', price_text)  # 15 USD
                if not price_match:
                    price_match = re.search(r'цена:\s*(\d+)', price_text, re.IGNORECASE)  # цена: 15

                if price_match:
                    price_pack_plans = int(price_match.group(1))
                    lst_prices.append(price_pack_plans)
                    print(f"Добавлено число: {price_pack_plans}")
                else:
                    raise ValueError(
                        f"Не удалось распознать цену: '{price_text}'. "
                        f"Ожидались форматы: $число, число USD, цена: число. "
                        f"Кнопка: {pack_plans[i]}"
                    )

        print(f"Итоговый список цен: {lst_prices}")
        return lst_prices

    def check_logic_pack_and_prices(self, pack_plans, lst_prices):
        # Проверяем что каждый следующий элемент больше предыдущего
        for i in range(1, len(pack_plans)):
            if pack_plans[i] <= pack_plans[i - 1]:
                raise ValueError(f"Нарушение прогрессии пакетов: {pack_plans[i - 1]} -> {pack_plans[i]}")

        for i in range(1, len(lst_prices)):
            if lst_prices[i] <= lst_prices[i - 1]:
                raise ValueError(f"Нарушение прогрессии цен: {lst_prices[i - 1]} -> {lst_prices[i]}")

        print("Логика прогрессии цен и пакетов не нарушена")
        return True

    def get_prices_per_download(self, pack_plans):
        lst_prices_per_download = []

        for i in range(len(pack_plans)):
            one_pack = wait_element(self.driver, LocatorsPlansAndPrisesPage.get_pack_credit_locator(pack_plans[i]), timeout=10)

            if one_pack:
                one_pack.click()
                one_price = wait_element(self.driver, LocatorsPlansAndPrisesPage.one_price_per_download, timeout=10)

                if not one_price:
                    raise Exception(f"Не найден элемент с ценой после клика на кнопку с числом {pack_plans[i]}")

                price_text = one_price.text.strip()
                print(f"Текст элемента: '{price_text}'")

                # Проверяем формат $0.53 за загрузку
                price_match = re.search(r'\$(\d+\.?\d*)\s*за\s*загрузку', price_text)

                if price_match:
                    price_pack_plans = float(price_match.group(1))
                    lst_prices_per_download.append(price_pack_plans)
                    print(f"Добавлено число: {price_pack_plans}")
                else:
                    raise ValueError(
                        f"Не удалось распознать цену: '{price_text}'. "
                        f"Ожидался формат: $число за загрузку. "
                        f"Кнопка: {pack_plans[i]}"
                    )

        print(f"Итоговый список цен за загрузку: {lst_prices_per_download}")
        return lst_prices_per_download

    def check_logic_prices_per_download(self, lst_prices_per_download):
        # Проверяем что каждый следующий элемент цен за загрузку больше или равен предыдущему
        for i in range(1, len(lst_prices_per_download)):
            if lst_prices_per_download[i] > lst_prices_per_download[i - 1]:
                raise ValueError(
                    f"Нарушение прогрессии цен за загрузку: {lst_prices_per_download[i - 1]} -> {lst_prices_per_download[i]}")

        print("Логика прогрессии цен за загрузку не нарушена")
        return True

    def go_month_tariff(self):
        wait_element(self.driver, LocatorsPlansAndPrisesPage.month_tariff, timeout=10).click()

    def check_month_tariff_active(self):
        try:
            # Находим элемент
            element = wait_element(self.driver, LocatorsPlansAndPrisesPage.month_tariff, timeout=10)

            # Получаем его классы
            classes = element.get_attribute("class")

            # Проверяем есть ли там магический класс
            if FlagActivePage.flag_check_active_tariff in classes:
                print("Выбран режим помесячного тарифа")
                return True
            else:
                print("Выбран другой режим, ошибка")
                return False

        except:
            print("Элемент не найден")
            return False

    def comparison_lst_price(self, lst_price_month, lst_price_annual):
        for i in range(len(lst_price_month)):
            if lst_price_annual[i] > lst_price_month[i]:
                return False
        print("Проверка прошла успешна, годовые цены пакетов меньше или равны месячным, что соответствует требованиям")
        return True

    def comparison_lst_price(self, lst_price_month, lst_price_annual):
        for i in range(len(lst_price_month)):
            if lst_price_annual[i] > lst_price_month[i]:
                return False
        print("Проверка прошла успешна, годовые цены пакетов меньше или равны месячным, что соответствует требованиям")
        return True

    def comparison_lst_price_per_download(self, prices_per_download_month, prices_per_download_annual):
        for i in range(len(prices_per_download_month)):
            if prices_per_download_annual[i] > prices_per_download_month[i]:
                return False
        print("Проверка прошла успешна, годовые цены за загрузку меньше или равны месячным, что соответствует требованиям")
        return True





