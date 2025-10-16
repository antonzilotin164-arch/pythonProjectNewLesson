from selenium.webdriver.common.by import By


class LocatorsLoginPage:
    button_entrance_locator = (By.XPATH, "//a[@data-cy=\"global-nav-sign-in-link\"]")
    email_locator = (By.XPATH, "//input[@id=\"new_session_username\"]")
    password_locator = (By.XPATH, "//input[@id=\"new_session_password\"]")
    entrance_locator = (By.XPATH, "//button[@id=\"sign_in\"]")
    button_accountIcon_locator = (By.XPATH, "//button[@data-testid=\"AccountIcon\"]")


class LocatorsRegistrationPage:
    button_create_locator = (By.XPATH, "//a[@class=\"create-account-button\"]")
    button_email_locator = (By.XPATH, "//input[@id=\"register_email\"]")
    button_password_locator = (By.XPATH, "//input[@id=\"register_password\"]")
    button_confirmation_locator = (By.XPATH, "//input[@id=\"register_password_confirmation\"]")
    button_regist_locator = (By.XPATH, "//button[@id=\"register-button\"]")
    button_accountIcon_locator = (By.XPATH, "//button[@data-testid=\"AccountIcon\"]")
    error_existing = (By.XPATH, "//*[contains(text(), 'адрес электронной почты уже существует')]")
    #Найти причину !!!
    error_confirmation_not_match = (By.XPATH, "//*[contains(text(), 'Пароли не совпадают')]")
    # error_confirmation_not_match = (By.XPATH, "//*[contains(text(), 'Пароли не совпадают')]")

class LocatorsAddUser:
    error_locator = (By.XPATH, "//*[contains(text(), 'адрес электронной почты уже существует')]")

class LocatorsMainPage:
    search_field = (By.XPATH, "//div[@data-testid=\"container-search-box\"]")
    input_field = (By.XPATH, "//input[@aria-label=\"text\"]")
    list_query = (By.XPATH, "//ul[@data-testid=\"suggestions-list\"]")
    value_field = (By.XPATH, "//input[@data-testid=\"container-search-box-input\"]")
    list_items = (By.XPATH, "//ul[@data-testid='suggestions-list']/li")
