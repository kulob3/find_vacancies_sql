import psycopg2
from psycopg2 import sql
from config import config


class DBManager:
    def __init__(self, database_name='vacancies'):
        self.conn = psycopg2.connect(dbname=database_name, **config())

    def get_companies_and_vacancies_count(self):
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
        vacancies = []
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.employer as company_name, v.name as vacancy_name, v.salary, v.currency, v.experience, v.employment, v.area, v.published_at, v.alternate_url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                LIMIT 100
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

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(CAST(salary AS INTEGER))
                FROM vacancies
                WHERE salary IS NOT NULL AND salary != 'Не указана'
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
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

    def close(self):
        self.conn.close()

# db_manager = DBManager()
# print(db_manager.get_companies_and_vacancies_count())
# print(db_manager.get_all_vacancies())
# print(db_manager.get_avg_salary())
# print(db_manager.get_vacancies_with_higher_salary())
# print(db_manager.get_vacancies_with_keyword('python'))
# db_manager.close()




