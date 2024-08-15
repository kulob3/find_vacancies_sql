from src.user_interface import create_request_phrase, option_sort, made_sql
from src.db_manager import DBManager

def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print('Привет! С помощью этой программы ты можешь найти работу.')
    vacancies = create_request_phrase()
    made_sql(vacancies)
    db_manager = DBManager()
    option_sort(db_manager)
    # print(f'Найдено {len(vacancies)} вакансий:')
    # js = JsonWorker()  # создаем объект класса JsonWorker
    # opend_json = js.open_file() # открываем файл json
    # change_currency_to_rub = change_currency(opend_json) # конвертируем зарплату в рубли из USD
    # option_sort(change_currency_to_rub)
    # while True: # цикл для повтора действий с вакансиями
    #     repeat_program = input(
    #         'Для возврата в меню выбора режима просмотра вакансий введите "1", для удаления вакансий и завершения работы программы введите "2": ')
    #     if repeat_program == '1':
    #         option_sort(change_currency_to_rub)
    #     elif repeat_program == '2':
    #         js.delete_file()
    #         break
    #     else:
    #         print("Неверный ввод. Пожалуйста, введите '1' или '2'.")
    print("Конец программы")


if __name__ == "__main__":
    user_interaction()