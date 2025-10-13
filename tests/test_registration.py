import pytest

from page.loginPage import LoginPage
from page.registrationPage import RegistrationPage
from utilities.fileOperations import save_email
from base.initializationDriver import *
from base.globalVariables import password

driver = initialization()

@pytest.mark.order(2)
def test_registration():
    login_page = LoginPage(driver)
    registration_page = RegistrationPage(driver)
    login_page.go_login_page()
    registration_page.go_registration_page()
    email = registration_page.start_registration()
    assert email is not None
    registration_page.enter_email(email)
    registration_page.enter_password(password)
    registration_page.enter_password_confirm(password)
    registration_page.registration_click()
    assert registration_page.check_user_not_existing()



@pytest.mark.order(2)
def test_reg_wrong_confirmation():
    login_page = LoginPage(driver)
    registration_page = RegistrationPage(driver)
    login_page.go_login_page()
    registration_page.go_registration_page()
    email = registration_page.start_registration()
    assert email is not None
    registration_page.enter_email(email)
    registration_page.enter_password(password)
    registration_page.enter_password_confirm("123")
    registration_page.registration_click()
    assert registration_page.check_password_match()