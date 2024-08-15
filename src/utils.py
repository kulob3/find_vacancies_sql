import requests
from src.vacancies import Vacancies

def get_exchange_rate():
    """
    Получает текущий курс обмена рубля к доллару США.
    Использует API Центрального Банка России.
    """
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        response = requests.get(url, timeout=10)  # Установка времени ожидания запроса 10 секунд
        response.raise_for_status()
        data = response.json()
        return data['Valute']['USD']['Value']
    except requests.RequestException as e:
        print(f"Ошибка при получении курса валюты: {e}. Курс валюты установлен по умолчанию: ")
        return 90.0



def vacansies_sort(list_vacancies):
    """
    Сортирует список вакансий по порядку
    """
    sorted_vacancies = []
    for i in list_vacancies:
        sorted_vacancies.append(
            Vacancies(i['vacancy_name'], i['company_name'], i['salary'], i['currency'], i['experience'],
                      i['employment'], i['area'], i['published_at'], i['alternate_url']))
    return sorted_vacancies