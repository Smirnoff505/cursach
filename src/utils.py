from src.class_api import HeadHunterAPI, SuperJobAPI


def select_platform(number: str):
    hh_api = HeadHunterAPI()
    sj_api = SuperJobAPI()

    if number in ['1', '2', '3']:
        if number == '1':
            return hh_api, None

        elif number == '2':
            return None, sj_api

        elif number == '3':
            return hh_api, sj_api

    else:
        print('Не выбрана ни одна платформа')
        quit()
