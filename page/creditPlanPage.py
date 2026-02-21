import re
from locators.locators import LocatorsCreditPlans
from base.globalVariables import add_value_url_for_plans_and_prices, basis_current_url_for_page_plans_and_prises
from base.initializationDriver import *
from base.flagActivePage import FlagActivePage

class CreditPlans:
    def __init__(self, driver):
        self.driver = driver

    def go_credit_plans_page(self):
        button_credit_plans = wait_element(self.driver, LocatorsCreditPlans.credit_plans, timeout=10)
        button_credit_plans.click()

    def check_selected_page(self):
        try:
            # Находим элемент
            button_credit_plans = wait_element(self.driver, LocatorsCreditPlans.credit_plans, timeout=10)

            # Получаем его классы
            classes_button_credit_plans = button_credit_plans.get_attribute("class")

            if FlagActivePage.flag_active_credit_plans_page in classes_button_credit_plans:
                print("Выбран режим кредитных пакетов")
                return True
            else:
                print("Выбран другой режим, это не соответствие требованиям")
                return False

        except:
            print("Элемент не найден")
            return False

    def get_value_credit_plans(self):
        buttons_credit_plans = wait_elements(self.driver, LocatorsCreditPlans.value_credit_plans, timeout=10)
        print(f"Найдено кнопок: {len(buttons_credit_plans)}")
        lst_credit_plans = []

        for i, button in enumerate(buttons_credit_plans):
            text = button.text.strip()
            print(f"Элемент {i + 1}: '{text}'")

            # Проверяем различные форматы с кредитами
            if not re.match(r'^\d+\s+Кредит(а|ов|а/ов)?$', text):
                print(f"Элемент не соответствует формату: '{text}'")
                return False

            # Извлекаем число
            number_match = re.search(r'^(\d+)', text)
            if number_match:
                credit_value = int(number_match.group(1))
                lst_credit_plans.append(credit_value)
            else:
                print(f"Не найдено число в тексте: '{text}'")
                return False

        print(f"Полученные значения пакетов: {lst_credit_plans}")
        return lst_credit_plans

    def get_prices(self):
        prices_plans = wait_elements(self.driver, LocatorsCreditPlans.price_credit_plans, timeout=10)
        print(f"Найдено элементов с ценами: {len(prices_plans)}")

        lst_prices = []
        for price in prices_plans:
            price_text = price.text.strip()
            print(f"Исходный текст: '{price_text}'")

            # Проверяем несколько возможных форматов с учетом запятых как разделителей тысяч
            price_match = re.search(r'\$([\d,]+)', price_text)  # $1,188
            if not price_match:
                price_match = re.search(r'([\d,]+)\s*USD', price_text)  # 1,188 USD
            if not price_match:
                price_match = re.search(r'цена:\s*\$?\s*([\d,]+)', price_text, re.IGNORECASE)  # цена: 1,188

            if price_match:
                # Убираем запятые и преобразуем в число
                price_str = price_match.group(1).replace(',', '')
                price_value = int(price_str)
                lst_prices.append(price_value)
                print(f"Добавлена цена: ${price_value} (из '{price_match.group(1)}')")
            else:
                raise ValueError(
                    f"Не удалось распознать цену: '{price_text}'. "
                    f"Ожидались форматы: $число, число USD, цена: число."
                )

        print(f"Итоговый список цен: {lst_prices}")
        return lst_prices

    def get_discounts(self):
        discounts = wait_elements(self.driver, LocatorsCreditPlans.discount, timeout=10)
        print(f"Найдено элементов: {len(discounts)}")
        lst_discounts = [0, 0]  # Начальные нули

        for i, discount in enumerate(discounts):
            text = discount.text.strip()
            print(f"Элемент {i + 1}: '{text}'")

            if not re.match(r'^Экономия\s*\$\s*(\d+)\*\*$', text):
                raise ValueError(
                    f"Элемент {i + 1} не соответствует формату скидки.\n"
                    f"Получено: '{text}'\n"
                    f"Ожидалось: 'Экономия $число**'"
                )

            discount_match = re.search(r'\$(\d+)', text)
            discount_value = int(discount_match.group(1))
            lst_discounts.append(discount_value)
            print(f"Найдена скидка: ${discount_value}")

        # Проверяем, что добавились реальные значения (длина списка больше 2)
        if len(lst_discounts) == 2:
            print("Не найдено ни одной скидки")
            return False

        print(f"Полученные значения скидок: {lst_discounts}")
        return lst_discounts

    def get_value_credit_button(self, lst_credit_plans):
        lst_value_credit_button = []

        for credit_value in lst_credit_plans:
            print(f"Обрабатываем кредитный план: {credit_value}")

            # Находим элемент по значению кредитов
            one_credit_plan = wait_element(self.driver, LocatorsCreditPlans.get_one_credit_plan(credit_value),
                                           timeout=10)

            if not one_credit_plan:
                raise Exception(f"Не найден элемент для кредитного плана: {credit_value}")

            # Кликаем на элемент
            one_credit_plan.click()
            time.sleep(0.2)  # Даем время для обновления DOM

            # Ищем кнопку с текущим значением
            one_value_credit_button = wait_element(self.driver, LocatorsCreditPlans.value_credit_button, timeout=10)

            if not one_value_credit_button:
                raise Exception(f"Не найден элемент с кнопкой после клика на план с числом {credit_value}")

            credit_button_text = one_value_credit_button.text.strip()
            print(f"Текст элемента: '{credit_button_text}' для плана {credit_value}")

            # Проверяем несколько возможных форматов
            credit_match = re.search(r'Купить\s+кредиты:\s*(\d+)', credit_button_text)
            if not credit_match:
                credit_match = re.search(r'Купить\s+(\d+)\s+кредит(?:а|ов)?', credit_button_text)

            if credit_match:
                extracted_value = int(credit_match.group(1))
                print(f"Извлечено значение: {extracted_value}, ожидалось: {credit_value}")

                # Проверяем, что извлеченное значение соответствует ожидаемому
                if extracted_value != credit_value:
                    print(f"ВНИМАНИЕ: Несоответствие! Ожидалось {credit_value}, но найдено {extracted_value}")

                lst_value_credit_button.append(extracted_value)
            else:
                raise ValueError(
                    f"Не удалось распознать количество кредитов: '{credit_button_text}'. "
                    f"Ожидались форматы: 'Купить кредиты: число' или 'Купить число кредит(а/ов)'. "
                    f"Кнопка: {credit_value}"
                )

            # Небольшая пауза между итерациями
            # time.sleep(0.5)

        print(f"Итоговый список кредитов: {lst_value_credit_button}")
        return lst_value_credit_button

    def compare_len_lst(self, lst_credit_plans, lst_prices, lst_discounts):
        len_credit = len(lst_credit_plans)
        len_prices = len(lst_prices)
        len_discounts = len(lst_discounts)

        if len_credit != len_prices or len_credit != len_discounts:
            raise ValueError(
                f"Длины списков не совпадают:\n"
                f"Кредитные планы: {len_credit} элементов\n"
                f"Цены: {len_prices} элементов\n"
                f"Скидки: {len_discounts} элементов"
            )

        print("Все списки имеют одинаковую длину")
        return True

    def check_logic_credit_plans_prices_discounts(self, lst_credit_plans, lst_prices, lst_discounts):
        # Проверяем что каждый следующий элемент больше предыдущего
        for i in range(1, len(lst_credit_plans)):
            if lst_credit_plans[i] <= lst_credit_plans[i - 1]:
                raise ValueError(f"Нарушение прогрессии кредитных планов: {lst_credit_plans[i - 1]} -> {lst_credit_plans[i]}")

        for i in range(1, len(lst_prices)):
            if lst_prices[i] <= lst_prices[i - 1]:
                raise ValueError(f"Нарушение прогрессии цен: {lst_prices[i - 1]} -> {lst_prices[i]}")

        for i in range(1, len(lst_discounts)):
            if lst_discounts[i] < lst_discounts[i - 1]:
                raise ValueError(f"Нарушение прогрессии скидок: {lst_discounts[i - 1]} -> {lst_discounts[i]}")

        print("Логика прогрессии кредитных планов, цен и скидок не нарушена")
        return True

    def check_discount_less_than_price(self, lst_prices, lst_discounts):
        # Проверяем, что все скидки меньше соответствующих цен
        for i in range(len(lst_prices)):
            if lst_discounts[i] >= lst_prices[i]:
                raise ValueError(
                    f"Скидка не может быть больше или равна цене. "
                    f"Цена: ${lst_prices[i]}, Скидка: ${lst_discounts[i]}, "
                    f"Позиция: {i + 1}"
                )

        print("Все скидки меньше соответствующих цен")
        return True
