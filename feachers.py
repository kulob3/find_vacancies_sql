import requests

def find_employer_id_by_name(name: str) -> int:
    """Функция для поиска идентификатора работодателя по его названию.
    Возвращает идентификатор работодателя или None, если работодатель не найден.
    Не связана с main.py и другими модулями. Выполняется отдельно. """

    url = "https://api.hh.ru/employers"
    params = {'text': name, 'only_with_vacancies': True}
    response = requests.get(url, params=params)
    response.raise_for_status()
    employers = response.json().get('items', [])
    if employers:
        return employers[0]['id']
    else:
        print(f"Работодатель с именем '{name}' не найден.")
        return None

# Пример использования
name = user_input = input("Введите название работодателя: ")
employer_id = find_employer_id_by_name(name)
print(f"Идентификатор работодателя {name} : {employer_id}")