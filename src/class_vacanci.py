class Vacancy:
    def __init__(self, title, city, link, currency, salary, description, date):
        self.title = title
        self.city = city
        self.link = link
        self.currency = currency
        if self.currency == 'RUR' or self.currency == 'rub':
            self.salary = salary
        elif self.currency == 'USD':
            self.salary = int(salary) * 92
            self.currency = 'RUR'
        self.description = description
        self.date = date

    def __repr__(self):
        return f'{self.__class__.__name__}({self.title}, {self.link}, {self.currency}, {self.salary}, ' \
               f'{self.description}, {self.date})'

    def __str__(self):
        return f'Наименование вакансии: {self.title}\n' \
               f'Город: {self.city}\n' \
               f'Ссылка на вакансию: {self.link}\n' \
               f'Описание вакансии: {self.description}\n' \
               f'Зарплата от:  {self.salary} {self.currency}\n' \
               f'Дата создания вакансии: {self.date}\n'

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self.salary < other.salary


