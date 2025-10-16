import pytest
from base.initializationDriver import initialization, stop_driver

@pytest.fixture()
def setup(request):
    request.cls.driver = initialization
    #request.cls.screenshot(request.cls)
    yield
    stop_driver(request.cls.driver)


