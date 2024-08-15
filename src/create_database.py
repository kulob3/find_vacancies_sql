import psycopg2

def create_db(db_name, **config) -> None:
    '''Создание базы данных, если она не существует'''
    conn = psycopg2.connect(dbname='postgres', **config)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f"DROP DATABASE {db_name}")
    except Exception as e:
        print(f'Информация: {e}')
    finally:
        cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=db_name, **config)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id VARCHAR(255) NOT NULL,
                employer VARCHAR(255) NOT NULL
            )
        """)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                employer_id VARCHAR(255) NOT NULL,
                salary VARCHAR(255),
                currency VARCHAR(10),
                experience VARCHAR(255) NOT NULL,
                employment VARCHAR(255) NOT NULL,
                area VARCHAR(255) NOT NULL,
                published_at TIMESTAMP NOT NULL,
                alternate_url VARCHAR(255) NOT NULL
            );
        """)
    conn.commit()
    conn.close()


def save_data_to_db(data: list[dict], database_name: str, **config) -> None:
    """ Сохранение данных в базу данных """
    conn = psycopg2.connect(dbname=database_name, **config)

    with conn.cursor() as cur:
        for i in data:
            cur.execute("""
                INSERT INTO vacancies (
                    name, employer_id, salary, currency, experience, employment, area, published_at, alternate_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                i['name'],
                i['employer']['id'],
                i['salary']['from'] if i['salary'] else 'Не указана',
                i['salary']['currency'] if i['salary'] else '',
                i['experience']['name'],
                i['employment']['name'],
                i['area']['name'],
                i['published_at'],
                i['alternate_url']
            ))
        for i in data:
            cur.execute("""
                INSERT INTO employers (
                    employer_id, employer
                ) VALUES (%s, %s)
                """, (
                i['employer']['id'],
                i['employer']['name']
            ))

    conn.commit()
    conn.close()