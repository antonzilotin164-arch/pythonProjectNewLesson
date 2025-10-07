from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def wait_element(driver, locator):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
