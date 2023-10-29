import re
import csv
from prettytable import PrettyTable
import os
from typing import Callable
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

def correct_description(s: str) -> str:
    return s[:100] + "..." if len(s)>100 else s

def correct_key_skills(s: str) -> str:
    return s.replace(", ",'\n')[:100] + "..." if len(s)>100 else s.replace(", ",'\n')

def correct_salary_gross(salary_currency, salary_gross, salary_from, salary_to: str) -> str:
    return salary_from + ' - ' + salary_to + ' (' + salary_currency + ') ' + '(' + ("Без вычета налогов" if salary_gross =="Да" else "С вычетом налогов") + ')'

def correct_salary(s: str) -> str:
    c = 0
    salary = ""
    for  i in range(-1,-len(s)-1,-1):
        if c == 3:
            salary = ' ' + salary
            c = 0

        salary = s[i] + salary
        c+=1

    return salary

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

    for key in row:
        row[key] = (lambda x: d_money[row[x]] if row[x] in d_money.keys() else row[x])(key)
        row[key] = (lambda x: d_experience[row[x]] if row[x] in d_experience.keys() else row[x])(key)
        row[key] = (lambda x: '.'.join(list(reversed(row[x].split('T')[0].split('-')))) if x == "published_at" else row[x])(key)

    func = correct_salary
    salary_from = func(row["salary_from"].split('.')[0])
    salary_to = func(row["salary_to"].split('.')[0])

    func_description, func_key_skills, func_salary_gross= correct_description, correct_key_skills, correct_salary_gross
    d = {"name":row["name"],
         "description": func_description(row["description"]),
         "key_skills": func_key_skills(row["key_skills"]),
         "experience_id":row["experience_id"],
         "premium":row["premium"],
         "employer_name":row["employer_name"],
         "salary_gross": func_salary_gross(row["salary_currency"],row["salary_gross"], salary_from, salary_to),
         "area_name":row["area_name"],
         "published_at":row["published_at"]} 

    return d

def add_row(row: dict,t:PrettyTable,n:int, func: Callable ) -> None:
    d = func(row)
    l = list(d.values())
    l.insert(0,str(n))
    t.add_row(l, divider=True)


def print_vacancies(data_vacancies: list, dic_naming: dict, start,end: int, fields: list) -> None:
    if len(data_vacancies) == 0:
        print("Нет данных")
        return
    
    t = PrettyTable()
    t.align = 'l'
    t._max_width = {"Название" : 20, "Описание": 20,"Навыки" : 20, "Опыт работы": 20,"Премиум-вакансия" : 20,
                     "Компания": 20, "Оклад": 20, "Название региона":20, "Дата публикации вакансии":20}
    t.field_names = dic_naming.values()

    n = 1
    func = formatter
    for data in data_vacancies:
       add_row(data,t,n,func)
       n+=1
    
    print(t.get_string(start=start, end=end,fields = fields))

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

amount_strs = input()
if len(amount_strs) == 1:
    start = int(amount_strs) - 1 if int(amount_strs)!=0 else int(amount_strs)
    end = len(data_vacancies)
elif len(amount_strs) == 0:
    start = 0
    end = len(data_vacancies)
else:
    start = int(amount_strs.split(' ')[0])-1
    end = int(amount_strs.split(' ')[1])-1

fields = input()
fields = list(dic_naming.values()).copy() if len(fields) == 0 else (fields + ", №").split(", ")

print_vacancies(data_vacancies, dic_naming,start,end,fields)


