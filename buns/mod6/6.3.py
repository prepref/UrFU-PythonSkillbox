from dataclasses import dataclass 
import csv

currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}

@dataclass
class Vacancy:
    name: str
    salary_from: str
    salary_to: str
    salary_currency: str
    area_name: str
    published_at: str

file = input('Введите название файла: ')
profession = input('Введите название профессии: ')

def universal_parser_csv(file)->list:
        def csv_reader(file) -> list:
            l = list()
            with open(file, encoding='utf-8-sig') as file:
                for row in csv.DictReader(file, delimiter=','):
                    if '' not in row.values() and all(row.values()):
                        l.append(Vacancy(
                                row["name"],
                                float(row["salary_from"]),
                                float(row["salary_to"]),
                                row["salary_currency"],
                                row["area_name"],
                                int(row["published_at"].split('-')[0])))
                
            return l
    
        vacancies_objects = csv_reader(file)
        return vacancies_objects


vacancies_objects = universal_parser_csv(file)

def salary_levels_year(l: list) -> None:
    d = dict()
    for vacancy in l:
        d[vacancy.published_at] = d.get(vacancy.published_at,[]) + [(vacancy.salary_from+vacancy.salary_to)//2 * currency_to_rub[vacancy.salary_currency]]
    
    for key,value in d.items():
        d[key] = int(sum(value)/len(value))
    print(f'Динамика уровня зарплат по годам: {d}')
    return

def amount_vacancies_year(l: list) -> None:
    d = dict()
    for vacancy in l:
        d[vacancy.published_at] = d.get(vacancy.published_at,[]) + [1]
    
    for key,value in d.items():
        d[key] = sum(value)
    print(f'Динамика количества вакансий по годам: {d}')
    return

def salary_levels_profession_year(l: list) -> None:
    d = dict()
    for vacancy in l:
        if profession in vacancy.name:
            d[vacancy.published_at] = d.get(vacancy.published_at,[]) + [(vacancy.salary_from+vacancy.salary_to)//2 * currency_to_rub[vacancy.salary_currency]]
        else:
            d[vacancy.published_at] = d.get(vacancy.published_at,[]) + [0]

    
    for key,value in d.items():
        c = 0
        for i in value:
            if i!=0:
                c+=1
        d[key] = int(sum(value)/c) if c!= 0 else 0

    print(f'Динамика уровня зарплат по годам для выбранной профессии: {d}')
    return

def amount_vacancies_year_profession(l: list) -> None:
    d = dict()
    for vacancy in l:
        if profession in vacancy.name:
            d[vacancy.published_at] = d.get(vacancy.published_at,[]) + [1]
        else:
            d[vacancy.published_at] = d.get(vacancy.published_at,[]) + [0]
        
    for key,value in d.items():
        d[key] = sum(value)

    print(f'Динамика количества вакансий по годам для выбранной профессии: {d}')
    return

def salary_levels_city(l: list) -> None:
    d = dict()
    d_vacancies = dict()
    d_res = dict() 
    for vacancy in l:
        d[vacancy.area_name] = d.get(vacancy.area_name,[]) + [(vacancy.salary_from+vacancy.salary_to)//2 * currency_to_rub[vacancy.salary_currency]]
        d_vacancies[vacancy.area_name] = d_vacancies.get(vacancy.area_name,[]) + [1]

    for key,value in d_vacancies.items():
        d_vacancies[key] = sum(value)
    count_vacancies = sum(d_vacancies.values())  

    for key,value in d.items():
        if d_vacancies[key]/count_vacancies * 100 >= 1:
            d_res[key] = int(sum(value)//len(value))
    print(f'Уровень зарплат по городам (в порядке убывания): {dict(sorted(d_res.items(), key= lambda x: x[1], reverse=True)[:10])}')
    return

def share_of_vacancies_city(l: list) -> None:
    d = dict()
    d_res = dict()
    for vacancy in l:
        d[vacancy.area_name] = d.get(vacancy.area_name,[]) + [1]
    
    for key,value in d.items():
        d[key] = sum(value)

    count_vacancies = sum(d.values())    
    for key in d:
        if d[key]/count_vacancies * 100 >= 1:
            d_res[key] = round(d[key]/count_vacancies,4)
    print(f'Доля вакансий по городам (в порядке убывания): {dict(sorted(d_res.items(), key= lambda x: x[1], reverse=True)[:10])}')
    return

salary_levels_year(vacancies_objects)
amount_vacancies_year(vacancies_objects)
salary_levels_profession_year(vacancies_objects)
amount_vacancies_year_profession(vacancies_objects)
salary_levels_city(vacancies_objects)
share_of_vacancies_city(vacancies_objects)