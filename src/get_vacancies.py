from abc import ABC, abstractmethod
import requests

class VacancyServiceAPI(ABC):
    """Абстрактный класс для работы с API сервиса вакансий"""
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def load_vacancies(self, query):
        pass

class HHruAPI(VacancyServiceAPI):
    ''' Класс для загрузки вакансий с HH.ru '''

    __base_url = "https://api.hh.ru/vacancies"

    def connect(self):
        """Функция для установления соединения с HH.ru"""
        try:
            response = requests.get(self.__base_url)
            response.raise_for_status()
            print("Соединение с HH.ru установлено")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка соединения: {e}")

    def load_vacancies(self, query):
        """Функция для загрузки вакансий с HH.ru"""
        params = {'employer_id': query, 'page': 0, 'per_page': 100}
        vacancies = []
        while params.get('page') != 20:
            response = requests.get(self.__base_url, params=params)
            vacancies.extend(response.json()['items'])
            params['page'] += 1
        return vacancies



