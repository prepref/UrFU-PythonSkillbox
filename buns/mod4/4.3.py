import re
import csv
from prettytable import PrettyTable
import os

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

def formatter(row: dict) -> dict:
    d_money = {"AZN": "Манаты",
                "BYR": "Белорусские рубли",
                "EUR": "Евро",
                "GEL": "Грузинский лари",
                "KGS": "Киргизский сом",
                "KZT": "Тенге",
                "RUR": "Рубли",
                "UAH": "Гривны",
                "USD": "Доллары",
                "UZS": "Узбекский сум"}
    d_experience = {
        "noExperience": "Нет опыта",
        "between1And3": "От 1 года до 3 лет",
        "between3And6": "От 3 до 6 лет",
        "moreThan6": "Более 6 лет"}

    for key,value in row.items():
        if value in d_money.keys():
            row[key] = d_money[value]
        if value in d_experience.keys():
            row[key] = d_experience[value]
        if key == "published_at":
            row[key] = '.'.join(list(reversed(value.split('T')[0].split('-'))))

    salary_from = ""
    c = 0
    a = row["salary_from"].split('.')[0]
    for  i in range(-1,-len(a)-1,-1):
        if c == 3:
            salary_from = ' ' + salary_from
            c = 0

        salary_from = a[i] + salary_from
        c+=1

    salary_to = ""
    c = 0
    a = row["salary_to"].split('.')[0]
    for  i in range(-1,-len(a)-1,-1):
        if c == 3:
            salary_to = ' ' + salary_to
            c = 0
        salary_to = a[i] + salary_to
        c+=1 

    d = {"name":row["name"],
         "description":row["description"][:100] + "..." if len(row["description"])>100 else row["description"],
         "key_skills":row["key_skills"].replace(", ",'\n')[:100] + "..." if len(row["key_skills"])>100 else row["key_skills"].replace(", ",'\n'),
         "experience_id":row["experience_id"],
         "premium":row["premium"],"employer_name":row["employer_name"],
         "salary_gross": salary_from + ' - ' + salary_to
             + ' (' + row["salary_currency"] + ') ' + '(' + ("Без вычета налогов" if row["salary_gross"]=="Да" else "С вычетом налогов") + ')',
         "area_name":row["area_name"],"published_at":row["published_at"]} 

    return d

def print_vacancies(data_vacancies: list, dic_naming: dict) -> None:
    if len(data_vacancies) == 0:
        print("Нет данных")
        return
    
    t = PrettyTable()
    t.align = 'l'
    t._max_width = {"Название" : 20, "Описание": 20,"Навыки" : 20, "Опыт работы": 20,"Премиум-вакансия" : 20,
                     "Компания": 20, "Оклад": 20, "Название региона":20, "Дата публикации вакансии":20}
    t.field_names = dic_naming.values()
    n = 1
    for data in data_vacancies:
        d = formatter(data)
        l = list(d.values())
        l.insert(0,str(n))
        t.add_row(l, divider=True)
        n += 1
    
    print(t)

file = input()
if os.stat(file).st_size == 0:
    print("Пустой файл")
    exit()

reader, list_naming = csv_reader(file)

data_vacancies = csv_filer(reader,list_naming)

dic_naming = {"number":"№","name":"Название","description":"Описание","key_skills":"Навыки",
               "experience_id":"Опыт работы", "premium":"Премиум-вакансия",
                "employer_name":"Компания",
                "salary_gross":"Оклад",
                "area_name":"Название региона", "published_at":"Дата публикации вакансии"}

print_vacancies(data_vacancies, dic_naming)


