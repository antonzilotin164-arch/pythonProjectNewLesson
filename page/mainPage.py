from selenium.webdriver import Keys
from locators.locators import LocatorsMainPage
from base.globalVariables import search_value, basis_current_url_for_page_search_image, add_value_url_for_search_image
from base.initializationDriver import *

class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def click_search_field(self):
        search_field = wait_element(self.driver, LocatorsMainPage.search_field, timeout=10)
        search_field.click()

    def input_search_query(self):
        input_field = wait_element(self.driver, LocatorsMainPage.input_field, timeout=10)
        input_field.send_keys(search_value)

    def check_input_value(self, search_value):
        input_field = wait_element(self.driver, LocatorsMainPage.input_field, timeout=5)
        actual_value = input_field.get_attribute("value")

        if actual_value == search_value:
            print(f"В поле поиска введено корректное значение: '{actual_value}'")
            return True
        else:
            print(f"Ошибка! Введено: '{actual_value}', ожидалось: '{search_value}'")
            return False

    def check_list_query(self):
        try:
            wait_element(self.driver, LocatorsMainPage.list_query, timeout=5)
            print("Нашел список")
            return True
        except TimeoutException:
            return False

    def get_list_query_texts(self):
        #Находим все элементы списка
        list_items = wait_elements(self.driver, LocatorsMainPage.list_items, timeout=5)
        #Получаем список, хранящий значения вариантов поиска
        texts = [item.text for item in list_items if item.text.strip()]
        return texts

    def check_value_elements(self, search_value,  texts):
        for text in texts:
            if search_value.lower() in text.lower():
                return True

        print(f"Ни один элемент не содержит слово '{search_value}'")
        return False

    def enter_to_search(self):
        enter_to_search = wait_element(self.driver, LocatorsMainPage.value_field, timeout=10)
        enter_to_search.send_keys(Keys.ENTER)

    # def check_current_url(self):
    #     wait_url(self.driver, timeout=10)
    #     get_current_url = self.driver.current_url
    #     encoded_search_value = urllib.parse.quote(search_value)
    #     factory_current_url = basis_current_url_for_page_search_image + encoded_search_value
    #     if get_current_url == factory_current_url:
    #         print(f"Мы находимся на правильной странице с картиками, которые относятся к поисковому слову {search_value}")
    #         return True
    #     else:
    #         print("Сбой, что-то пошло не так")
    #         return False

    def check_current_url(self):
        result = check_current_url(self.driver, basis_current_url_for_page_search_image, add_value_url_for_search_image)
        if result:
            print(f"Мы находимся на правильной странице с картиками, которые относятся к поисковому слову {search_value}")
            return result
        else:
            print("Сбой, что-то пошло не так")
            return result





