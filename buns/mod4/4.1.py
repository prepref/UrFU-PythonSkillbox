import re
import csv

def csv_reader(file_name:str) -> (list,list):
    reader = list()
    list_naming = list()
    with open(file_name, encoding='utf-8-sig') as file:
        count = 0
        for row in csv.reader(file, delimiter=','):
            if count == 0:
                list_naming = row
                count += 1
            else:
                reader.append(row)
    
    return reader, list_naming


def csv_filer(reader, list_naming: list) -> list:
    data_vacancies = list()

    for data in reader:
        if '' not in data and len(data) == len(list_naming):
            d = dict()
            data[0] = data[0].replace('\xa0',' ')
            data[1] = re.sub(r'[ ]+',' ',re.sub(r'<.*?>', '', data[1]).strip())
            data[1] = data[1].replace('  ',' ').replace('\xa0',' ')
            data[2] = ', '.join(data[2].split('\n'))
            data[-1] = data[-1].replace('\xa0', ' ')
            data[4] = data[4].replace('FALSE', 'Нет').replace('TRUE', 'Да').replace('False', 'Нет').replace('True', 'Да')
            data[8] = data[8].replace('FALSE', 'Нет').replace('TRUE', 'Да').replace('False', 'Нет').replace('True', 'Да')
            for i in range(len(data)):
                d[list_naming[i]] = data[i]

            data_vacancies.append(d)

    return data_vacancies

def print_vacancies(data_vacancies: list, dic_naming: dict) -> None:
    for data in data_vacancies:
        for key,value in data.items():
            print(dic_naming[key] + ': ' + str(value))
        if data_vacancies.index(data) != len(data_vacancies)-1:
            print('')

reader, list_naming = csv_reader(input())

data_vacancies = csv_filer(reader,list_naming)

dic_naming = {"name":"Название","description":"Описание","key_skills":"Навыки",
               "experience_id":"Опыт работы", "premium":"Премиум-вакансия",
                "employer_name":"Компания", "salary_from":"Нижняя граница вилки оклада",
                "salary_to":"Верхняя граница вилки оклада", "salary_gross":"Оклад указан до вычета налогов",
                "salary_currency":"Идентификатор валюты оклада",
                "area_name":"Название региона", "published_at":"Дата и время публикации вакансии"}

print_vacancies(data_vacancies, dic_naming)


