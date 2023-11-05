import re
import csv
import os
from var_dump import var_dump

class Salary:
    def __init__(self,salary_from,salary_to,salary_gross,salary_currency) -> None:
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

class Vacancy:
    def __init__(self,name,description,key_skills,experience_id,premium,employer_name,salary,area_name,published_at) -> None:
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at

class DataSet:
    def __init__(self, file_name, vacancies_objects) -> None:
        self.file_name = file_name
        self.vacancies_objects = vacancies_objects


file = input('Введите название файла: ')
filtr = input('Введите параметр фильтрации: ')
sort_parametr = input('Введите параметр сортировки: ')
reverse_sort = input('Обратный порядок сортировки (Да / Нет): ')
amount_strs = input('Введите диапазон вывода: ')
fields = input('Введите требуемые столбцы: ')

if os.stat(file).st_size == 0:
    print("Пустой файл")
    exit()

def universal_parser_csv(file:str)->list:
    def csv_filer(reader: list, list_naming: list):
        l = list()
        for data in reader:
            if '' not in data and len(data) == len(list_naming):
                l.append(Vacancy(
                data[0].replace('\xa0',' '),
                re.sub(r'[ ]+',' ',re.sub(r'<.*?>', '', data[1]).strip()).replace('  ',' ').replace('\xa0',' '),
                data[2].split('\n'),
                data[3],
                data[4],
                data[5],
                Salary(data[6],
                        data[7],
                        data[8],
                        data[9]),
                data[10],
                data[11]))

        return l

    def csv_reader(file: str) -> list:
        reader = list()
        list_naming = list()
        with open(file, encoding='utf-8-sig') as file:
            count = 0
            for row in csv.reader(file, delimiter=','):
                if count == 0:
                    list_naming = row
                    count += 1
                else:
                    reader.append(row)
            
        return csv_filer(reader,list_naming)
    
    vacancies_objects = csv_reader(file)
    return vacancies_objects

var_dump(DataSet(file, universal_parser_csv(file)))





