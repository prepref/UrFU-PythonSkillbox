import csv

# В папке есть csv файл c данными из задания(также я немного я его сам дополнил случайными данными), чтобы вы могли проверить, что все работает как надо

# Задание 2.1
# Проверяет, есть ли в строке значения, длина которых равна 0
def ValidateRows(row) -> bool:
    for i in row:
        i = " ".join(str(i).split())
        if len(i) == 0:
            return False
    
    return True

# Проверяет, есть ли в csv пустые значения и правильно ли заполнены данные
def ValidateCSV(name: str) -> (list(), list(list())):
    fields_head = list()
    fields = list(list())
    with open(name, 'r', encoding="utf8") as file:
        r = csv.reader(file, delimiter=",")
        count = 0
        length = 0
        for row in r:
            if count == 0:
                length = len(row)
                fields_head = row
                count += 1
            else:
                if len(row) == length and ValidateRows(row):
                    fields.append(row)
    return fields_head, fields

# Задание 2.2
# Удаляет html теги
def RemoveHTML_Tags_ForString(value: str)-> str:
    s = ""
    f = True

    for i in value:
        if i == "<":
            f = False
        if f:
            s += str(i)
        if i == ">":
            f = True

    return s

# Удаляет лишние пробелы в начале, конце и середине значений
def RemoveSpace(fields: list(list())) -> list(list()):
    new_fields = list(list())

    for field in fields:
        l = list()
        for i in field:
            if isinstance(i, list) == False:
                i = RemoveHTML_Tags_ForString(i)
                i = " ".join(str(i).split())
                l.append(i)
            else:
                in_l = list()
                for j in i:
                    j = RemoveHTML_Tags_ForString(str(j))
                    j = " ".join(str(j).split())
                    in_l.append(j)
                
                l.append(in_l)

        new_fields.append(l)

    return new_fields

# Разбивает строки, которые содержат "\n" на list
def ToList(fields: list(list())) -> list(list()):
    new_fields = list(list())
    for field in fields:
        l = list()
        for i in field:
            if "\n" in str(i):
                i = str(i).split("\n")
            l.append(i)

        new_fields.append(l)  

    return new_fields                        

# Возвращает csv в виде словаря
def CSV_ToDict(fields_head: list(), fields: list(list())) -> list(dict()):
    new_fields = ToList(fields)
    new_fields = RemoveSpace(new_fields)

    dict_fields = list(dict())

    for field in new_fields:
        d = dict()
        for i in range(len(field)):
            d[fields_head[i]] = field[i]

        dict_fields.append(d)
    
    return dict_fields

# Задание 2.3
# Считает процент числа вакансий в определённом городе от общего числа рублёвых вакансий
def SumRUR_Vacancies(n1: int, n2: int) -> bool:
    res = (n2 * 100) // n1
    if res < 1:
        return False
    return True

# Склоненяет слово "рубль"
def GetDeclinationRUR(n: int) -> str:
    s = ""
    if n%10 == 0 or 5 <=n%10 <=9:
        s = "рублей"
    elif n%10 == 1:
        s = "рубль"
    elif 2 <=n%10<= 4:
        s = "рубля"
    return s

# Склоненяет слово "раз"
def GetDeclinationCount(n: int) -> str:
    s = ""
    if 5 <=n%10<= 9:
        s = "раз"
    elif n%10 == 1 or n%10 == 0:
        s = "раз"
    elif 2 <=n%10<= 4:
        s = "раза"
    return s

# Склоненяет слово "вакансия"
def GetDeclinationVacancies(n: int) -> str:
    s = ""
    if 5 <=n%10<= 9 or n%10 == 0:
        s = "вакансий"
    elif n%10 == 1:
        s = "вакансия"
    elif 2 <=n%10<= 4:
        s = "вакансии"
    return s

# Общее число вакансий в RUR
def CountVacanciesRUR(l: list(dict())) -> int:
    count_vacancies = 0
    for field in l:
        if "RUR" in dict(field).values():
            count_vacancies += 1
    return count_vacancies

# Число вакансий в определённом городе
def CountVacanciesArea(l: list(dict())) -> dict:
    area_name = "area_name"
    d_area_name = dict()
    for field in l:
        if "RUR" in dict(field).values():
            if field[area_name] not in d_area_name.keys():
                d_area_name[field[area_name]] = 1
            else:
                d_area_name[field[area_name]] += 1
    
    return d_area_name

# Возвращает список словарей, где только те города, в которых число вакансий больше 1% от общего числа рублёвых вакансий 
def GetCorrectlyArea(l: list(dict())) -> list(dict()):
    l_new = list(dict())
    count_vacancies = CountVacanciesRUR(l)
    d_area_name = CountVacanciesArea(l)
    f = True

    for field in l:
        if "RUR" in dict(field).values():
            for key,_ in dict(field).items():
                if key == "area_name":
                    f = SumRUR_Vacancies(count_vacancies,d_area_name[key])
                if f:
                    l_new.append(field)
                    break
    
    return l_new

# Выводит список самых высоких и низких зарплат
def ListSalaries(l: list(dict()))-> None:
    d_high = dict()
    name, employer_name, area_name, salary_from, salary_to, salary_corrency = "name", "employer_name", "area_name", "salary_from", "salary_to", "salary_corrency"

    print("Самые высокие зарплаты:")

    for field in l:
        d_high[(int(field[salary_from])+int(field[salary_to]))//2] = [field[name], field[employer_name], field[area_name]]

    # d_high - словарь самых высоких зарплат, где значение - массив
    # d_high - словарь самых низких зарплат, где значение - массив
    d_high = sorted(d_high.items())
    d_low = d_high
    d_high = reversed(d_high)
    n = 1

    for key,value in dict(d_high).items():
        s = GetDeclinationRUR(key)
        print(" {}) {} в компании \"{}\" - {} {} (г. {})".format(n, value[0], value[1], key, s, value[2]))
        n += 1
        if n>10:
            break
    
    print("\n")
    print("Самые низкие зарплаты:")

    n = 1

    for key,value in dict(d_low).items():
        s = GetDeclinationRUR(key)
        print(" {}) {} в компании \"{}\" - {} {} (г. {})".format(n, value[0], value[1], key, s, value[2]))
        n += 1
        if n>10:
            break

# Выводит список популярных навыков
def ListSkills(l: list(dict())) -> None:
    d = dict()
    key_skills = "key_skills"
    count = 0

    # Проверка на тип, так как если это не list то, по циклу не надо прогонять
    for field in l:
        if isinstance(field[key_skills],list):
            for i in field[key_skills]:
                if i not in d.keys():
                    d[i] = 1
                    count += 1
                else:
                    d[i] += 1
        else:
            if field[key_skills] not in d.keys():
                d[field[key_skills]] = 1
                count += 1
            else:
                d[field[key_skills]] += 1
    
    print("Из {} скиллов, самыми популярными являются:".format(count))

    # d - словарь со скилами и их количеством упоминаний
    d = sorted(d.items(), key=lambda item: item[1], reverse=True)

    n = 1
    for key, value in dict(d).items():
        s = GetDeclinationCount(value)
        print(" {}) {} - упоминается {} {}".format(n, key, value, s))
        n += 1
        if n > 10:
            break

# Выводит список средних зарплат
def ListMediumSalaries(l: list(dict())) -> None:
    d = dict()
    area_name = "area_name"
    salary_from, salary_to = "salary_from", "salary_to"
    count = 0
    d_area_name = CountVacanciesArea(l)

    for key,_ in d_area_name.items():
        count += 1

    for field in l:
        if field[area_name] not in d.keys():
            d[field[area_name]] = (int(field[salary_from])+int(field[salary_to]))//2
        else:
            d[field[area_name]] += (int(field[salary_from])+int(field[salary_to]))//2
    
    print("Из {} городов, самые высокие средние ЗП:".format(count))

    for key,value in dict(d).items():
        d[key] = value//d_area_name[key]

    # d - словарь, где ключ - город, а значение - средняя зарплата в городе
    d = sorted(d.items(), key=lambda item: item[1], reverse=True)
    n = 1

    for key, value in dict(d).items():
        s = GetDeclinationRUR(value)
        s_area = GetDeclinationVacancies(d_area_name[key])
        print(" {}) {} - средняя зарплата {} {} ({} {})".format(n, key, value, s, d_area_name[key], s_area))
        n += 1
        if n > 10:
            break

# Выводит CSV заданному формату в  заданиях 2.1, 2.2, 2.3
def OutputCorrectlyCSV(name: str) -> None:
     # Задание 2.1
    fields_head = list()
    fields = list(list())
    count = 0

    file_validate = ValidateCSV(name)

    for field in file_validate:
        if count == 0:
            fields_head = list(field)
            count += 1
        else:
            fields = list(field)

    print("Задание 1")
    print(fields_head)
    print(fields)
    print("\n")

    # Задание 2.2
    out_as_dict = CSV_ToDict(fields_head,fields)

    print("Задание 2")

    for field in out_as_dict:
        for key, value in dict(field).items():
            s = ""
            if isinstance(value, list):
                for i in value:
                    s += str(i) + ", "
                print(key + ": " + s[:len(s)-2])
                s = ""
            else:
                print(key + ": " + value)
        
        print("\n")

    # Задание 2.3
    out_as_dict_new = GetCorrectlyArea(out_as_dict)
    print("Задание 3")
    ListSalaries(out_as_dict_new)
    print("\n")
    ListSkills(out_as_dict_new)
    print("\n")
    ListMediumSalaries(out_as_dict_new)
    print("\n")

if __name__ == "__main__":
    OutputCorrectlyCSV('./vacancies.csv')

    
