import pytest
from base.initializationDriver import initialization, stop_driver

@pytest.fixture()
def setup(request):
    request.cls.driver = initialization
    #request.cls.screenshot(request.cls)
    yield
    stop_driver(request.cls.driver)

@pytest.fixture(scope="session")
def duplicate_check_status():
    """
    Фикстура для хранения статуса проверки на дубликаты в течение всей сессии.
    """
    return {"passed": False}
