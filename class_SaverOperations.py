from abc import ABC, abstractmethod
import json
import os
import csv


class SaveOperations(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def add_vacancy(self):
        pass


class JSONSaver(SaveOperations):
    def __init__(self):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def add_vacancy(self, vacancies: list):
        file_path = os.path.abspath('data/vacancies.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, indent=2, ensure_ascii=False)


class CSVSaver(SaveOperations):
    def __init__(self):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def add_vacancy(self, vacancies: list):
        file_path = os.path.abspath('data/vacancies.csv')
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'link', 'city', 'salary_currency', 'salary_from',
                                                   'salary_to', 'description', 'date'])
            for vacancy in vacancies:
                writer.writerow(vacancy)
