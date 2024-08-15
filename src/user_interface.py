from config import config
from src.get_vacancies import HHruAPI
from src.create_database import create_db, save_data_to_db
from src.utils import vacansies_sort

def create_request_phrase():
    '''Функция для формирования и получения поискового запроса.'''
    hh = HHruAPI()  # Создаем объект класса HHruAPI
    hh.connect()  # Устанавливаем соединение с HH.ru
    vacancies = hh.load_vacancies(['1740', '592442', '1455', '15478', '9459850', '3127', '3086759', '4592004', '567049', '10814600', '4219'])
    return vacancies

def made_sql(vacancies):
    '''Функция для создания базы данных'''
    create_db('vacancies', **config())  # создаем базу данных
    save_data_to_db(vacancies, 'vacancies', **config())  # записываем данные в базу данных


def option_sort(db_manager):
    """Функция для выбора действий с вакансиями"""
    vacancies_for_output = []
    while True:
        value_for_sort = input(
            "Введите '1' для просмотра количества вакансий у работодателей, '2' для поиска вакансий по ключевому слову, '3' для вывода вакансий с зарплатой выше среднего уровня, '4' - без сортировки: ")
        if value_for_sort == '1':
            company_list = db_manager.get_companies_and_vacancies_count()
            for i in company_list:
                print(f'Работодатель: {i["company_name"]}, количество вакансий: {i["vacancies_count"]}')
            break
        elif value_for_sort == '2':
            keyword =  input("Введите ключевое слово для поиска вакансий: ")
            vacancies_for_output = vacansies_sort(db_manager.get_vacancies_with_keyword(keyword))
            if not vacancies_for_output:
                print("Вакансий по данному запросу не найдено.")
            break
        elif value_for_sort == '3':
            vacancies_for_output = vacansies_sort(db_manager.get_vacancies_with_higher_salary())
            break
        elif value_for_sort == '4':
            vacancies_for_output = vacansies_sort(db_manager.get_all_vacancies())
            break
        else:
            print("Неверный ввод. Пожалуйста, введите '1', '2', '3' или '4'.")
    if len(vacancies_for_output) <= 20:
            for i in vacancies_for_output:
                print(i.__str__())
    else:
        batch_size = 20
        for start in range(0, len(vacancies_for_output), batch_size):
            end = start + batch_size
            for vacancy in vacancies_for_output[start:end]:
                print(vacancy.__str__())
            user_input = input("\nВведите 1, чтобы увидеть следующие вакансии или 2 для окончания просмотра: ")
            if user_input != '1':
                break







