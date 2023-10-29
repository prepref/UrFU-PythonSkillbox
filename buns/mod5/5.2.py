import re
import csv
from prettytable import PrettyTable, ALL
import os
from typing import Callable

dic_naming = {"number":"№","name":"Название","description":"Описание","key_skills":"Навыки",
               "experience_id":"Опыт работы", "premium":"Премиум-вакансия",
                "employer_name":"Компания",
                "salary_gross":"Оклад",
                "area_name":"Название региона", "published_at":"Дата публикации вакансии"}

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
            data[-1] = data[-1].replace('\xa0', ' ')
            data[4] = data[4].replace('FALSE', 'Нет').replace('TRUE', 'Да').replace('False', 'Нет').replace('True', 'Да')
            data[8] = data[8].replace('FALSE', 'Нет').replace('TRUE', 'Да').replace('False', 'Нет').replace('True', 'Да')
            for i in range(len(data)):
                d[list_naming[i]] = data[i]

            data_vacancies.append(d)

    return data_vacancies

def correct(s: str) -> str:
    return (s[:100] + "...") if len(s)>100 else s

def correct_key_skills(s: str) -> str:
    return (s[:100] + "...") if len(s)>=100 else s

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

def formatter(row: dict, n:int, filtr:str) -> dict:

    for key in row:
        row[key] = (lambda x: d_money[row[x]] if row[x] in d_money.keys() else row[x])(key)
        row[key] = (lambda x: d_experience[row[x]] if row[x] in d_experience.keys() else row[x])(key)
        row[key] = (lambda x: '.'.join(list(reversed(row[x].split('T')[0].split('-')))) if x == "published_at" else row[x])(key)

    func = correct_salary
    salary_from = func(row["salary_from"].split('.')[0])
    salary_to = func(row["salary_to"].split('.')[0])

    func_correct, func_key_skills, func_salary_gross= correct, correct_key_skills, correct_salary_gross

    return {"name":func_correct(row["name"]),
         "description": func_correct(row["description"]),
         "key_skills": func_key_skills(row["key_skills"]),
         "experience_id":func_correct(row["experience_id"]),
         "premium":func_correct(row["premium"]),
         "employer_name":func_correct(row["employer_name"]),
         "salary_gross": func_salary_gross(row["salary_currency"],row["salary_gross"], salary_from, salary_to),
         "area_name":func_correct(row["area_name"]),
         "published_at":func_correct(row["published_at"])}

def add_row(row: dict,t:PrettyTable,n:int, func: Callable,filtr:str ) -> None:
    d = func(row,n,filtr)
    l = list(d.values())
    l.insert(0,str(n))
    t.add_row(l)

def filtrate(data_vacancies: list, filtr:str) -> list:
    if filtr == "" or filtr.split(': ')[1] == "":
        return data_vacancies
    elif filtr.split(": ")[0] in ["Название","Описание","Компания", "Название региона"]:
        data_vacancies_new = (lambda x: [i for i in x if filtr.split(": ")[1] in list(i.values())])(data_vacancies)
    elif filtr.split(": ")[1].count('.') == 2:
        data_vacancies_new = (lambda x: [i for i in x if '.'.join(list(reversed(i["published_at"].split('T')[0].split('-')))) == filtr.split(": ")[1]])(data_vacancies)
    elif filtr.split(': ')[1] in d_experience.values():
        data_vacancies_new = (lambda x: [i for i in x if d_experience[i["experience_id"]] == filtr.split(': ')[1]])(data_vacancies)
    elif filtr.split(': ')[0] == "Навыки":
        data_vacancies_new = list()
        for data in data_vacancies:
            c = 0
            for i in filtr.split(': ')[1].split(', '):
                if i in data["key_skills"].split('\n'):
                    c+=1
            if c==len(filtr.split(': ')[1].split(', ')):
                data_vacancies_new.append(data)
    elif filtr.split(': ')[0] == 'Оклад' and filtr.split(": ")[1][-1] not in 'йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjklzxcvbnm.ЙЦУКЕНГШЩЗФЫВАПРОЛДЯЧСМИТЬБЮЭQWERTYUIOPASDFGHJKLZXCVBNM':
        data_vacancies_new = (lambda x: [i for i in x if int(i["salary_from"].split('.')[0]) <= int(filtr.split(": ")[1]) <= int(i["salary_to"].split('.')[0])])(data_vacancies)
    elif filtr.split(": ")[0] == "Премиум-вакансия":
        data_vacancies_new = (lambda x: [i for i in x if filtr.split(": ")[1] == i["premium"]])(data_vacancies)
    elif 'Идентификатор валюты оклада' in filtr.split(': ')[0]:
        data_vacancies_new = (lambda x: [i for i in x if d_money[i["salary_currency"]] == filtr.split(': ')[1]])(data_vacancies)
    else:
        data_vacancies_new = []
    
    return data_vacancies_new
    

def print_vacancies(data_vacancies: list, dic_naming: dict, st,en: int, fi: list, filtr: str) -> None:
    if len(data_vacancies) == 0:
        print("Нет данных")
        return
    
    t = PrettyTable()
    t.hrules = ALL
    t.align = 'l'
    t._max_width = {"№":20,"Название" : 20, "Описание": 20,"Навыки" : 20, "Опыт работы": 20,"Премиум-вакансия" : 20,
                     "Компания": 20, "Оклад": 20, "Название региона":20, "Дата публикации вакансии":20}
    t.field_names = dic_naming.values()

    n = 1
    func = formatter
    func_filter = filtrate
    data_vacancies_new = func_filter(data_vacancies,filtr)
    if len(data_vacancies_new) == 0:
        print("Ничего не найдено")
        return
    for data in data_vacancies_new:
       add_row(data,t,n,func,filtr)
       n+=1
    
    print(t.get_string(start=st, end=en,fields = fi))

file = input()
if os.stat(file).st_size == 0:
    print("Пустой файл")
    exit()

filtr = input()
if len(filtr) > 0 and ': ' not in filtr:
    print("Формат ввода некорректен")
    exit()
if len(filtr) > 0 and filtr.split(': ')[0] not in ["Навыки","Оклад","Дата публикации вакансии","Опыт работы","Премиум-вакансия","Идентификатор валюты оклада","Название","Название региона","Компания"]:
    print("Параметр поиска некорректен")
    exit()

reader, list_naming = csv_reader(file)

data_vacancies = csv_filer(reader,list_naming)

amount_strs = input()
if ' ' not in amount_strs and len(amount_strs)>0:
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

print_vacancies(data_vacancies, dic_naming,start,end,fields,filtr)


