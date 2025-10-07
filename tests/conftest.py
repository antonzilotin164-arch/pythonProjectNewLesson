import pytest

@pytest.fixture(scope="session")
def duplicate_check_status():
    """
    Фикстура для хранения статуса проверки на дубликаты в течение всей сессии.
    """
    return {"passed": False}