from abc import ABC, abstractmethod
import requests
import time

class VacancyServiceAPI(ABC):
    """Абстрактный класс для работы с API сервиса вакансий"""

    @abstractmethod
    def load_vacancies(self, query):
        pass

class HHruAPI(VacancyServiceAPI):
    ''' Класс для загрузки вакансий с HH.ru '''

    __base_url = "https://api.hh.ru/vacancies"

    def load_vacancies(self, query):
        """Функция для загрузки вакансий с HH.ru"""
        params = {'employer_id': query, 'page': 0, 'per_page': 100}
        vacancies = []
        retries = 2
        while params.get('page') != 20:
            for i in range(retries):
                try:
                    response = requests.get(self.__base_url, params=params)
                    response.raise_for_status()
                    vacancies.extend(response.json()['items'])
                    break
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка соединения: {e}.\nПовторная попытка...")
                    time.sleep(3)  #  Повтор через 3 секунды
            else:
                print("Не удалось подключиться к API после нескольких попыток.")
                break
            params['page'] += 1
        print("Соединение с HH.ru установлено") if vacancies else print("Соединение с HH.ru не установлено")
        return vacancies



