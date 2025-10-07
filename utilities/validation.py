from utilities.fileOperations import load_all_emails
def validate_email(email):
    existing_emails = load_all_emails()
    if email in existing_emails:
        print("Данный пользователь уже зарегистрирован")
        return False
    if '@' not in email:
        print("Ошибка: Email должен содержать @")
        return False
    if len(email) > 254:
        print("Ошибка: Email слишком длинный")
        return False
    if '.' not in email.split('@')[1]:
        print("Ошибка: Доменная часть должна содержать точку")
        return False
    if email.startswith('.'):
        print("Ошибка: Email не может начинаться с точки")
        return False
    if email.endswith('.'):
        print("Ошибка: Email не может заканчиваться точкой")
        return False
    return True
