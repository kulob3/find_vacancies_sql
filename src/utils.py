from src.vacancies import Vacancies


def vacansies_sort(list_vacancies):
    """
    Сортирует список вакансий
    """
    sorted_vacancies = []
    for i in list_vacancies:
        sorted_vacancies.append(
            Vacancies(i['vacancy_name'], i['company_name'], i['salary'], i['currency'], i['experience'],
                      i['employment'], i['area'], i['published_at'], i['alternate_url']))
    return sorted_vacancies