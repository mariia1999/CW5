import psycopg2
from utils.config import config


class DBManager:
    def __init__(self, db_name):
        self.__db_name = db_name

    def __execute_query(self, query):
        con = psycopg2.connect(dbname=self.__db_name, **config())
        with con:
            with con.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        con.close()
        return result

    def get_companies_and_vacancies_count(self):
        query = ("SELECT e.name, COUNT(v.id) AS vacancy_count FROM employers e "
                 "JOIN vacancies v ON e.id = v.employer GROUP BY e.name")
        return self.__execute_query(query)

    def get_all_vacancies(self):
        query = ("SELECT * FROM vacancies "
                 "JOIN employers ON vacancies.employer = employers.id")
        return self.__execute_query(query)

    def get_avg_salary(self):
        query = "SELECT AVG(salary_from) FROM vacancies"
        return self.__execute_query(query)

    def get_vacancies_with_higher_salary(self):
        query = "SELECT salary_from FROM vacancies ORDER BY salary_from DESC"
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, user_query):
        query = f"SELECT * FROM vacancies WHERE name LIKE '%{user_query}%'"
        return self.__execute_query(query)

