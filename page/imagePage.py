from locators.locators import LocatorsImagePage
from base.globalVariables import base_url_image_page, add_url_image_page, request
from base.initializationDriver import *
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)
class ImagePage():
    def __init__(self, driver):
        self.driver = driver

    def check_current_url(self):
        result = check_current_url(self.driver, base_url_image_page, add_url_image_page)
        if result:
            logger.info("Мы успешно попали на ресурс генерации изображений")
            return result
        else:
            logger.info("Сбой, что-то пошло не так")
            return result

    def check_current_model_generate(self):
        model_generate = wait_element(self.driver, LocatorsImagePage.model_generate, timeout=10)
        css_style_color = model_generate.value_of_css_property("color")
        if css_style_color in ["rgb(255, 255, 255)", "rgba(255, 255, 255, 1)", "#fff", "#ffffff"]:
            logger.info("Выбрана модель по умолчанию")
            return True
        else:
            logger.info("Ошибка выбора модели генерации")
            return False

    def select_model_generate(self):
        selected_model_generate = wait_element(self.driver, LocatorsImagePage.selected_model_generate, timeout=10)
        selected_model_generate.click()

    def check_selected_model(self):
        check_model = wait_element(self.driver, LocatorsImagePage.selected_model_generate, timeout=10)
        font_weight = check_model.value_of_css_property("font-weight")
        if font_weight in ["bold", "700", "600"]:
            logger.info("Модель выбрана верно")
            return True
        else:
            logger.info(f"Модель выбрана неверно")
            return False

    def click_descriptions_field(self):
        descriptions_field = wait_element(self.driver, LocatorsImagePage.descriptions_field, timeout=10)
        descriptions_field.click()

    def check_input_field_is_active(self):
        time.sleep(0.5)
        input_field_is_active = wait_element(self.driver, LocatorsImagePage.descriptions_field, timeout=10)
        css_style_border_color = input_field_is_active.value_of_css_property("border-color")

        #Отладочный вывод
        logger.info(f"Фактический цвет границы: '{css_style_border_color}'")

        #Разные возможные форматы цвета
        expected_colors = ["#e253dd", "rgb(226, 83, 221)", "rgba(226, 83, 221, 1)"]

        if css_style_border_color in expected_colors:
            logger.info("Поле ввода активно")
            return True
        else:
            logger.info(f"Ошибка, поле ввода неактивно. Ожидался один из: {expected_colors}")
            return False

    def input_descriptions_query(self):
        input_descriptions_field = wait_element(self.driver, LocatorsImagePage.descriptions_field, timeout=10)
        input_descriptions_field.send_keys(request)

    def check_value(self, search_value, locator):
        field_value = wait_element(self.driver, locator, timeout=5)
        actual_value = field_value.get_attribute("value")

        if actual_value == search_value:
            logger.info(f"В поле корректное значение: '{actual_value}'")
            return True
        else:
            logger.info(f"Ошибка!: '{actual_value}', ожидалось: '{search_value}'")
            return False

    # МЕТОДЫ СКАЧИВАНИЯ
    def click_button_generate_image(self, locator):
        button_generate_image = wait_element(self.driver, locator, timeout=5)
        button_generate_image.click()

    def check_click_button_generate_image(self):
        generate_button = wait_element(self.driver, LocatorsImagePage.button_generate_image, timeout=10)
        is_disabled = generate_button.get_attribute("disabled") is not None
        if is_disabled:
            logger.info("Кнопка 'Сгенерировать изображение' заблокирована")
        else:
            logger.info("Кнопка 'Сгенерировать изображение' активна")
        return is_disabled

    def check_start_generation(self):
        loading_indicator = wait_element(self.driver, LocatorsImagePage.loading_indicator, timeout=10)
        display_value = loading_indicator.value_of_css_property("display")

        if display_value == "block":
            logger.info("Генерация изображения начата успешно")
            return True
        elif display_value == "none":
            logger.info("Генерация изображения провалилась")
            return False

    def click_download_button(self):
        """Нажимает кнопку Скачать с ожиданием и скроллом"""

        # Ждем пока элемент станет кликабельным
        download_element = WebDriverWait(self.driver, 300).until(
            EC.element_to_be_clickable(LocatorsImagePage.download_button_complet)
        )

        # Скроллим к элементу
        self.driver.execute_script("arguments[0].scrollIntoView(true);", download_element)
        time.sleep(1)

        # Пробуем кликнуть через JavaScript
        self.driver.execute_script("arguments[0].click();", download_element)

    def handle_save_dialog(self):
        """Закрывает системный диалог 'Сохранить как'"""
        import pyautogui
        time.sleep(2)
        pyautogui.press('enter')

    def wait_for_download_complete(self, timeout=10):
        downloads_dir = Path.home() / "Downloads"
        target_dir = Path(__file__).parent.parent / "downloads"
        target_dir.mkdir(exist_ok=True)

        logger.info(f"Ищем файлы в: {downloads_dir}")

        def _check_and_move_file():
            current_files = list(downloads_dir.glob("*"))
            logger.info(f"Найдено файлов: {len(current_files)}")

            completed_files = [f for f in current_files
                               if not f.name.endswith(('.crdownload', '.tmp', '.part'))]
            logger.info(f"Завершенные файлы: {[f.name for f in completed_files]}")

            image_files = [f for f in completed_files
                           if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp']]
            logger.info(f"Картинки: {[f.name for f in image_files]}")

            if image_files:
                newest_file = max(image_files, key=lambda f: f.stat().st_ctime)
                logger.info(f"Найдена картинка: {newest_file.name}")

                target_file = target_dir / newest_file.name
                newest_file.rename(target_file)
                return target_file
            return None

        wait = WebDriverWait(self.driver, timeout, poll_frequency=1)
        downloaded_file = wait.until(
            lambda driver: _check_and_move_file(),
            message="Скачивание картинки не завершилось"
        )
        return downloaded_file
