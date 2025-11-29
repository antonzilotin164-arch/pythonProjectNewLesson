from base.globalVariables import request, correct_aspect_ratio
from locators.locators import LocatorsImagePage
def test_open_browers(browser_session):
    #Шаг №1 - переход на ресурс генерации изображения
    driver, generate_image_page = browser_session

    # Шаг №2 - проверка, что открыт верный ресурс
    assert generate_image_page.check_current_url()

def test_check_model(browser_session):
    # Шаг №1 - переход на ресурс генерации изображения
    driver, generate_image_page = browser_session

    # Шаг №2 - проверка, что выбрана модель по умолчанию
    assert generate_image_page.check_current_model_generate()

def test_select_model(browser_session):
    # Шаг №1 - переход на ресурс генерации изображения
    driver, generate_image_page = browser_session

    # Шаг №2 - переход на модель FLUX.1 [pro]
    generate_image_page.select_model_generate()

    # Шаг №3 - проверка, что действительно перешли на модель FLUX.1 [pro]
    assert generate_image_page.check_selected_model()

def test_check_input_field_is_active(browser_session):
    # Шаг №1 - переход на ресурс генерации изображения
    driver, generate_image_page = browser_session

    # Шаг №2 - переход на модель FLUX.1 [pro]
    generate_image_page.select_model_generate()

    # Шаг №3 - клик по полю ввода
    generate_image_page.click_descriptions_field()

    # Шаг №4 - поверка, что поле ввода стало активно
    assert generate_image_page.check_input_field_is_active()

def test_input_field_accepts_and_displays_text(browser_session):
    # Шаг №1 - переход на ресурс генерации изображения
    driver, generate_image_page = browser_session

    # Шаг №2 - переход на модель FLUX.1 [pro]
    generate_image_page.select_model_generate()

    # Шаг №3 - клик по полю ввода
    generate_image_page.click_descriptions_field()

    # Шаг №4 - ввод запроса на генерацию изображения
    generate_image_page.input_descriptions_query()

    # Шаг №5 - проверка, что значение в поле ввода соответствует введенному запросу на генерацию изображения
    assert generate_image_page.check_value(request, LocatorsImagePage.descriptions_field)

def test_check_aspect_ratio(browser_session):
    # Шаг №1 - переход на ресурс генерации изображения
    driver, generate_image_page = browser_session

    # Шаг №2 - переход на модель FLUX.1 [pro]
    generate_image_page.select_model_generate()

    # Шаг №3 - клик по полю ввода
    generate_image_page.click_descriptions_field()

    # Шаг №4 - ввод запроса на генерацию изображения
    generate_image_page.input_descriptions_query()

    # Шаг №5 - проверка, что заданное разрешение изображения соответствует требованиям
    assert generate_image_page.check_value(correct_aspect_ratio, LocatorsImagePage.aspect_ratio)

def test_check_click_button_generate_image(browser_session):
    # Шаг №1 - переход на ресурс генерации изображения
    driver, generate_image_page = browser_session

    # Шаг №2 - переход на модель FLUX.1 [pro]
    generate_image_page.select_model_generate()

    # Шаг №3 - клик по полю ввода
    generate_image_page.click_descriptions_field()

    # Шаг №4 - ввод запроса на генерацию изображения
    generate_image_page.input_descriptions_query()

    # Шаг №5 - клик по кнопке "Сгенерировать изображение"
    generate_image_page.click_button_generate_image(LocatorsImagePage.button_generate_image)

    # Шаг №5 - проверка, что нажатие кнопки прошло успешно
    assert generate_image_page.check_click_button_generate_image()


def test_start_generation(browser_session):
    # Шаг №1 - переход на ресурс генерации изображения
    driver, generate_image_page = browser_session

    # Шаг №2 - переход на модель FLUX.1 [pro]
    generate_image_page.select_model_generate()

    # Шаг №3 - клик по полю ввода
    generate_image_page.click_descriptions_field()

    # Шаг №4 - ввод запроса на генерацию изображения
    generate_image_page.input_descriptions_query()

    # Шаг №5 - клик по кнопке "Сгенерировать изображение"
    generate_image_page.click_button_generate_image(LocatorsImagePage.button_generate_image)

    # Шаг №6 - проверка, что генерация изображения начата успешно
    assert generate_image_page.check_start_generation()

def test_check_file_download_successful(browser_session_with_download):
    # Шаг №1 - переход на ресурс генерации изображения, создание папки для скачивания
    driver, generate_image_page, download_dir = browser_session_with_download
    print(f"Папка для скачивания: {download_dir}")

    # Шаг №2 - переход на модель FLUX.1 [pro]
    generate_image_page.select_model_generate()

    # Шаг №3 - клик по полю ввода
    generate_image_page.click_descriptions_field()

    # Шаг №4 - ввод запроса на генерацию изображения
    generate_image_page.input_descriptions_query()

    # Шаг №5 - клик по кнопке "Сгенерировать изображение"
    generate_image_page.click_button_generate_image(LocatorsImagePage.button_generate_image)

    # Шаг №6 - нажатие кнопки скачивания
    generate_image_page.click_download_button()

    # Шаг №7 - обработка системного диалога
    generate_image_page.handle_save_dialog()

    # Шаг №9 - ожидание завершения скачивания
    downloaded_file = generate_image_page.wait_for_download_complete()

    # Шаг №10 - проверка, что скачивание завершено скачивания
    assert downloaded_file

