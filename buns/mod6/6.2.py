import re
import csv
import os
from var_dump import var_dump
from prettytable import PrettyTable, ALL

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

class Salary:
    def __init__(self,salary_from,salary_to,salary_gross,salary_currency) -> None:
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency
    def currency_transfer(self,s: str) -> str:
        return d_money[s] if s in d_money.keys() else s
    def gross_translate(self,s: str) -> str:
        return  s.replace('FALSE', 'Нет').replace('TRUE', 'Да').replace('False', 'Нет').replace('True', 'Да')
    def correct_salary(self,s: str) -> str:
        c = 0
        salary = ""
        for  i in range(-1,-len(s)-1,-1):
            if c == 3:
                salary = ' ' + salary
                c = 0

            salary = s[i] + salary
            c+=1

        return salary
    def correct_salary_gross(self) -> str:
            return self.correct_salary(self.salary_from.split('.')[0]) + ' - ' + self.correct_salary(self.salary_to.split('.')[0]) + ' (' + self.currency_transfer(self.salary_currency) + ') ' + '(' + ("Без вычета налогов" if self.gross_translate(self.salary_gross) =="Да" else "С вычетом налогов") + ')'

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
    def experience_id_translate(self,s: str) -> str:
        return d_experience[s] if s in d_experience.keys() else s
    def published_at_translate(self,s: str) -> str:
        return '.'.join(list(reversed(s.split('T')[0].split('-'))))
    def correct(self,s: str) -> str:
        return (s[:100] + "...") if len(s)>100 else s

    def correct_key_skills(self,s: str) -> str:
        return (s[:100] + "...") if len(s)>=100 else s
    def formatter(self):
        self.name = self.correct(self.name)
        self.description = self.correct(self.description)
        self.key_skills = self.correct_key_skills(self.key_skills)
        self.experience_id = self.correct(self.experience_id_translate(self.experience_id))
        self.premium = self.correct(self.premium)
        self.employer_name = self.correct(self.employer_name)
        self.salary = self.salary.correct_salary_gross()
        self.area_name = self.correct(self.area_name)
        self.published_at = self.correct(self.published_at_translate(self.published_at))
    def to_list(self) -> list:
        return [self.name,self.description,self.key_skills,self.experience_id,self.premium,self.employer_name,self.salary,self.area_name,self.published_at]

class DataSet:
    def __init__(self, file_name) -> None:
        self.file_name = file_name

    def universal_parser_csv(self)->list:
        file = self.file_name
        def csv_filer(reader: list, list_naming: list) -> list:
            l = list()
            for data in reader:
                if '' not in data and len(data) == len(list_naming):
                    l.append(Vacancy(
                    data[0].replace('\xa0',' '),
                    re.sub(r'[ ]+',' ',re.sub(r'<.*?>', '', data[1]).strip()).replace('  ',' ').replace('\xa0',' '),
                    data[2],
                    data[3],
                    data[4].replace('FALSE', 'Нет').replace('TRUE', 'Да').replace('False', 'Нет').replace('True', 'Да'),
                    data[5],
                    Salary(data[6],
                            data[7],
                            data[8],
                            data[9]),
                    data[10],
                    data[11].replace('\xa0', ' ')))

            return l

        def csv_reader(file) -> list:
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

class InputConect:
    def __init__(self,file,filtr,sort_parametr,reverse_sort,amount_strs,fields) -> None:
        self.file = file
        self.filtr = filtr
        self.sort_parametr = sort_parametr
        self.reverse_sort = reverse_sort
        self.amount_strs = amount_strs
        self.fields = fields
    def correct_file(self) -> str:
        if os.stat(self.file).st_size == 0:
            print("Пустой файл")
            return 'error'
        return self.file
    def correct_filtr(self) -> str:
        if len(self.filtr) > 0 and ': ' not in self.filtr:
            print("Формат ввода некорректен")
            return 'error'
        if len(self.filtr) > 0 and self.filtr.split(': ')[0] not in ["Навыки","Оклад","Дата публикации вакансии","Опыт работы","Премиум-вакансия","Идентификатор валюты оклада","Название","Название региона","Компания"]:
            print("Параметр поиска некорректен")
            return 'error'
        return self.filtr
    def correct_sort_parametr(self) -> str:
        if self.sort_parametr != "" and self.sort_parametr not in dic_naming.values():
            print("Параметр сортировки некорректен")
            return 'error'
        return self.sort_parametr
    def correct_reverse_sort(self) -> str:
        if self.reverse_sort == 'Да':
            return "True"
        elif self.reverse_sort == 'Нет' or self.reverse_sort == "":
            return "False"
        else:
            print("Порядок сортировки задан некорректно")
            return 'error'

    def correct_amount_strs(self) -> (int,int):
        if ' ' not in self.amount_strs and len(self.amount_strs)>0:
            start = int(self.amount_strs) - 1 if int(self.amount_strs)!=0 else int(self.amount_strs)
            end = -1
        elif len(self.amount_strs) == 0:
            start = 0
            end = -1
        else:
            start = int(self.amount_strs.split(' ')[0])-1
            end = int(self.amount_strs.split(' ')[1])-1  
        return start, end
    def correct_fields(self) -> str:
        return list(dic_naming.values()).copy() if len(self.fields) == 0 else (self.fields + ", №").split(", ")
    

file = input('Введите название файла: ')
filtr = input('Введите параметр фильтрации: ')
sort_parametr = input('Введите параметр сортировки: ')
reverse_sort = input('Обратный порядок сортировки (Да / Нет): ')
amount_strs = input('Введите диапазон вывода: ')
fields = input('Введите требуемые столбцы: ')

input_conect = InputConect(file,filtr,sort_parametr,reverse_sort,amount_strs,fields)

file = input_conect.correct_file()
filtr = input_conect.correct_filtr()
sort_parametr = input_conect.correct_sort_parametr()
reverse_sort = input_conect.correct_reverse_sort()
start, end = input_conect.correct_amount_strs()
fields = input_conect.correct_fields()

if file == 'error' or filtr == 'error' or sort_parametr == 'error' or reverse_sort == 'error':
    exit()
        
def filtrate(data_vacancies: list, filtr:str) -> list:
    if filtr == "" or filtr.split(': ')[1] == "":
        return data_vacancies
    elif filtr.split(": ")[0] in ["Название","Описание","Компания", "Название региона"]:
        data_vacancies_new = (lambda x: [i for i in x if filtr.split(": ")[1] in list(i.to_list())])(data_vacancies)
    elif filtr.split(": ")[1].count('.') == 2:
        data_vacancies_new = (lambda x: [i for i in x if '.'.join(list(reversed(i.published_at.split('T')[0].split('-')))) == filtr.split(": ")[1]])(data_vacancies)
    elif filtr.split(': ')[1] in d_experience.values():
        data_vacancies_new = (lambda x: [i for i in x if d_experience[i.experience_id] == filtr.split(': ')[1]])(data_vacancies)
    elif filtr.split(': ')[0] == "Навыки":
        data_vacancies_new = list()
        for data in data_vacancies:
            c = 0
            for i in filtr.split(': ')[1].split(', '):
                if i in data.key_skills.split('\n'):
                    c+=1
            if c==len(filtr.split(': ')[1].split(', ')):
                data_vacancies_new.append(data)
    elif filtr.split(': ')[0] == 'Оклад' and filtr.split(": ")[1][-1] not in 'йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjklzxcvbnm.ЙЦУКЕНГШЩЗФЫВАПРОЛДЯЧСМИТЬБЮЭQWERTYUIOPASDFGHJKLZXCVBNM':
        data_vacancies_new = (lambda x: [i for i in x if int(i.salary.salary_from.split('.')[0]) <= int(filtr.split(": ")[1]) <= int(i.salary.salary_to.split('.')[0])])(data_vacancies)
    elif filtr.split(": ")[0] == "Премиум-вакансия":
        data_vacancies_new = (lambda x: [i for i in x if filtr.split(": ")[1] == i.premium])(data_vacancies)
    elif 'Идентификатор валюты оклада' in filtr.split(': ')[0]:
        data_vacancies_new = (lambda x: [i for i in x if d_money[i.salary.salary_currency] == filtr.split(': ')[1]])(data_vacancies)
    else:
        data_vacancies_new = []
            
    return data_vacancies_new

def print_vacancies(data_vacancies: list, filtr: str, sort_parametr:str, reverse_sort: str,start:int,end:int,fields:list) -> None:
    if len(data_vacancies) == 0:
        print("Нет данных")
        return

    if reverse_sort == "True":
        f = True
    else:
        f = False

    if sort_parametr == "Оклад":
        data_vacancies.sort(key= lambda x: ((float(x.salary.salary_from)
                                            + float(x.salary.salary_to))//2)
                                             *float(currency_to_rub[x.salary.salary_currency]), reverse= f)

    t = PrettyTable()
    t.hrules = ALL
    t.align = 'l'
    t._max_width = {"№":20,"Название" : 20, "Описание": 20,"Навыки" : 20, "Опыт работы": 20,"Премиум-вакансия" : 20,
                    "Компания": 20, "Оклад": 20, "Название региона":20, "Дата публикации вакансии":20}
    t.field_names = dic_naming.values()

    n = 1
    data_vacancies_new = filtrate(data_vacancies,filtr)

    if len(data_vacancies_new) == 0:
        print("Ничего не найдено")
        return

    d_experience_id = {"Нет опыта":0,"От 1 года до 3 лет":1,"От 3 до 6 лет":2,"Более 6 лет":3}

    if sort_parametr == "Премиум-вакансия":
        data_vacancies_new.sort(key= lambda x: x.premium, reverse=f)
    elif sort_parametr == "Название":
        data_vacancies_new.sort(key= lambda x: x.name, reverse=f)
    elif sort_parametr == "Описание":
        data_vacancies_new.sort(key= lambda x: x.description, reverse=f)
    elif sort_parametr == "Компания":
        data_vacancies_new.sort(key= lambda x: x.employer_name, reverse=f)
    elif sort_parametr == "Название региона":
        data_vacancies_new.sort(key= lambda x: x.area_name, reverse=f)
    elif sort_parametr == "Опыт работы":
        data_vacancies_new.sort(key= lambda x: d_experience_id[d_experience[x.experience_id]], reverse=f)
    elif sort_parametr == "Дата публикации вакансии":
        data_vacancies_new.sort(key= lambda x: '.'.join(list(reversed(x.published_at.split('.')))), reverse=f)
    elif sort_parametr == "Навыки":
        data_vacancies_new.sort(key= lambda x: len(x.key_skills.split('\n')), reverse=f)

    for data in data_vacancies_new:
        data.formatter()
        l = data.to_list()
        l.insert(0,str(n))
        t.add_row(l)
        n+=1
    
    if end == -1:
        print(t.get_string(start=start, end=len(data_vacancies_new),fields = fields))
    else:
        print(t.get_string(start=start, end=end,fields = fields))

vacancies_objects = DataSet(file).universal_parser_csv()

print_vacancies(vacancies_objects,filtr,sort_parametr,reverse_sort,start,end,fields)









