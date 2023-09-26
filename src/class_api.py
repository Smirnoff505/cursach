import os
from abc import ABC, abstractmethod
from datetime import datetime

import requests


class API(ABC):

    def __init__(self):
        pass

    def __repr__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def parse_vacancies(self):
        pass


class HeadHunterAPI(API):
    """Подключается к API HeadHunter и получает список вакансий по заданным критериям"""

    def __init__(self):
        self.base_url = 'https://api.hh.ru'

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.base_url})'

    def get_vacancies(self, text: list, per_page=100) -> list:
        """
        Возвращает список вакансий по ключевому слову
        """

        url = f'{self.base_url}/vacancies'

        params = {
            # если город не введен поиск ведется по всей России (установлено по умолчанию)
            'area': 113,
            'text': text,
            # включает вакансии только с указанной зарплатой
            'only_with_salary': True,
            'per_page': per_page
        }

        response = requests.get(url, params=params)
        vacancies = response.json()['items']
        return vacancies

    def parse_vacancies(self, vacancies: dict) -> list:
        """Оставляем данные необходимые для дальнейшей работы"""
        lst_vacancies = []

        for vacancy in vacancies:
            # преобразовываем дату в читаемый вид
            date_obj = datetime.strptime(vacancy['published_at'][:10], '%Y-%m-%d')
            format_date = datetime.strftime(date_obj, '%d-%m-%Y')

            item = {
                'title': vacancy['name'],  # наименование вакансии
                'link': vacancy['alternate_url'],  # ссылка на вакансию
                'city': vacancy['area']['name'],  # город
                'salary_currency': vacancy['salary']['currency'],  # валюта
                'salary_from': vacancy['salary']['from'],  # нижняя планка зарплаты
                'salary_to': vacancy['salary']['to'],  # предел зарплаты
                'description': vacancy['snippet']['requirement'],  # краткое описание вакансии
                'date': format_date  # дата публикации вакансии
            }
            lst_vacancies.append(item)
        return lst_vacancies


class SuperJobAPI(API):
    api_key = os.getenv('SJ_API')

    def __init__(self):
        self.base_url = "https://api.superjob.ru/2.0"

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.base_url})'

    def get_vacancies(self, keyword, count=100):
        """
        Возвращает список вакансий по ключевому слову
        """
        url = f"{self.base_url}/vacancies"
        headers = {
            "X-Api-App-Id": self.api_key
        }
        params = {
            "keyword": keyword,
            'count': count,
            # если город не введен поиск ведется по всей России (установлено по умолчанию)
            'id': 1

        }
        response = requests.get(url, headers=headers, params=params)
        vacancies = response.json()['objects']
        return vacancies

    def parse_vacancies(self, vacancies: dict):
        """Оставляем данные необходимые для дальнейшей работы"""
        lst_vacancies = []

        for vacancy in vacancies:
            # преобразовываем дату в читаемый вид
            date = datetime.fromtimestamp(vacancy['date_pub_to'])
            format_date = date.strftime("%d-%m-%Y")

            item = {
                'title': vacancy['profession'],  # наименование вакансии
                'link': vacancy['link'],  # ссылка на вакансию
                'city': vacancy['town']['title'],  # город
                'salary_currency': vacancy['currency'],  # валюта
                'salary_from': vacancy['payment_from'],  # нижняя планка зарплаты
                'salary_to': vacancy['payment_to'],  # предел зарплаты
                'description': vacancy['work'],  # краткое описание вакансии
                'date': format_date  # дата публикации вакансии
            }
            lst_vacancies.append(item)
        return lst_vacancies
