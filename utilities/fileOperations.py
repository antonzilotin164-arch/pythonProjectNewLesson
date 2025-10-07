import re
from base.globalVariables import base_email


def load_all_emails():
    """Загружаем всю почту из файла"""
    try:
        with open('list_email.txt', 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []


def email_factory():
    """Генерируем новую почту на основе последней записи в файле"""
    emails = load_all_emails()

    # Если файл пустой, возвращаем base_email
    if not emails:
        return base_email

    # Берем последний email из файла
    last_email = emails[-1]

    # Извлекаем базовую часть username (без +number) и domain из base_email
    if '+' in base_email:
        base_users = base_email.split('+')[0]  # "zilotin164" из "zilotin164+1@gmail.com"
    else:
        base_users = base_email.split('@')[0]  # "zilotin164" из "zilotin164@gmail.com"

    domain = '@' + base_email.split('@')[1]  # "@gmail.com"

    # Ищем число после плюса в последнем email
    match = re.search(r'\+(\d+)(?=@)', last_email)

    if match:
        # Увеличиваем найденное число
        new_number = int(match.group(1)) + 1
        return f"{base_users}+{new_number}{domain}"
    else:
        # Если плюса нет, но email существует - добавляем +1
        return f"{base_users}+1{domain}"

def save_email(email):
    """Сохраняем почту в файл"""
    with open('list_email.txt', 'a') as f:
        f.write('\n' + email)