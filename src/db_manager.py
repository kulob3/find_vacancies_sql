import psycopg2
from psycopg2 import sql
from config import config


class DBManager:
    """Класс для работы с базой данных"""
    def __init__(self, database_name):
        self.conn = psycopg2.connect(dbname=database_name, **config())

    def get_companies_and_vacancies_count(self):
        """Функция для получения списка работодателей и количества вакансий у них"""
        companies = []
        with self.conn.cursor() as cur:
            cur.execute("""

                 SELECT e.employer as company_name, COUNT(v.id) as vacancies_count
                 FROM vacancies v
                 JOIN employers e ON v.employer_id = e.employer_id
                 GROUP BY e.employer
             """)
            for row in cur.fetchall():
                company = {
                    'company_name': row[0],
                    'vacancies_count': row[1]
                }
                companies.append(company)
        return companies

    def get_all_vacancies(self):
        """Функция для получения всех вакансий"""
        vacancies = []
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.employer as company_name, v.name as vacancy_name, v.salary, v.currency, v.experience, v.employment, v.area, v.published_at, v.alternate_url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                LIMIT 200
            """)
            for row in cur.fetchall():
                vacancy = {
                    'company_name': row[0],
                    'vacancy_name': row[1],
                    'salary': row[2],
                    'currency': row[3],
                    'experience': row[4],
                    'employment': row[5],
                    'area': row[6],
                    'published_at': row[7],
                    'alternate_url': row[8]
                }
                vacancies.append(vacancy)
        return vacancies

    def get_avg_salary(self):
        """Функция для получения средней зарплаты"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(CAST(salary AS INTEGER))
                FROM vacancies
                WHERE salary IS NOT NULL AND salary != 'Не указана'
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Функция для получения вакансий с зарплатой выше среднего уровня"""
        avg_salary = self.get_avg_salary()
        vacancies = []
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.employer as company_name, v.name as vacancy_name, v.salary, v.currency, v.experience, v.employment, v.area, v.published_at, v.alternate_url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.salary ~ '^\d+$' AND CAST(v.salary AS INTEGER) > %s
            """, (avg_salary,))
            for row in cur.fetchall():
                vacancy = {
                    'company_name': row[0],
                    'vacancy_name': row[1],
                    'salary': row[2],
                    'currency': row[3],
                    'experience': row[4],
                    'employment': row[5],
                    'area': row[6],
                    'published_at': row[7],
                    'alternate_url': row[8]
                }
                vacancies.append(vacancy)
        return vacancies

    def get_vacancies_with_keyword(self, keyword):
        """Функция для поиска вакансий по ключевому слову"""
        vacancies = []
        with self.conn.cursor() as cur:
            cur.execute(sql.SQL("""
                SELECT e.employer as company_name, v.name as vacancy_name, v.salary, v.currency, v.experience, v.employment, v.area, v.published_at, v.alternate_url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE v.name ILIKE %s
            """), (f'%{keyword}%',))
            for row in cur.fetchall():
                vacancy = {
                    'company_name': row[0],
                    'vacancy_name': row[1],
                    'salary': row[2],
                    'currency': row[3],
                    'experience': row[4],
                    'employment': row[5],
                    'area': row[6],
                    'published_at': row[7],
                    'alternate_url': row[8]
                }
                vacancies.append(vacancy)
        return vacancies






