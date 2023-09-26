from src.class_vacanci import Vacancy
from class_SaverOperations import JSONSaver, CSVSaver
from src.utils import select_platform


def user_interaction():
    choose_platform = input(f'1 - HeadHunter\n'
                            f'2 - SuperJob\n'
                            f'3 - HeadHunter + SuperJob\n'
                            f'Выберите платформу на которой будет осуществляться поиск: ')

    hh_api, sj_api = select_platform(choose_platform)

    while True:
        search_query = input("Введите ключевые слова (Например, python): ").split()
        if len(search_query) >= 1:
            break
        elif search_query == []:
            print('Это поле не может быть пустым')

    search_city = input('Введите город или нажмите Enter для поиска по России: ')
    if search_city == '':
        pass
    else:
        search_query.append(search_city)

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))

    print()
    print(f'Поиск будет произведен на: {hh_api}, {sj_api}\n'
          f'Ключевые слова: {search_query}\n'
          f'Вакансии будут отсортированы по зарплате начиная с самой высокой.\n'
          f'В результате поиска будут выведены первые {top_n} вакансий')
    input()

    if not hh_api is None:
        hh_vacancies = hh_api.get_vacancies(','.join(search_query))
        parse_vacancies_hh = hh_api.parse_vacancies(hh_vacancies)
    else:
        parse_vacancies_hh = []

    if not sj_api is None:
        sj_vacancies = sj_api.get_vacancies(' '.join(search_query))
        parse_vacancies_sj = sj_api.parse_vacancies(sj_vacancies)
    else:
        parse_vacancies_sj = []

    full_vacancies = parse_vacancies_hh + parse_vacancies_sj

    JSONSaver().add_vacancy(full_vacancies)
    CSVSaver().add_vacancy(full_vacancies)

    # создание списка классов Vacancy полученных с HeadHunter и SuperJob
    list_vacancies = []
    for item in full_vacancies:
        # если в вакансии в поле зарплата_до не None зарплату заполняем, иначе устанавливаем 0
        if item['salary_from'] is not None:
            list_vacancies.append(
                Vacancy(item['title'],
                        item['city'],
                        item['link'],
                        item['salary_currency'],
                        item['salary_from'],
                        item['description'],
                        item['date']))
        else:
            list_vacancies.append(
                Vacancy(item['title'],
                        item['city'],
                        item['link'],
                        item['salary_currency'],
                        0,
                        item['description'],
                        item['date']))

    sorted_vacancies = sorted(list_vacancies, reverse=True)

    if len(sorted_vacancies) < top_n:
        for i in range(len(sorted_vacancies)):
            print(sorted_vacancies[i])
    else:
        for i in range(top_n):
            print(sorted_vacancies[i])

    return
