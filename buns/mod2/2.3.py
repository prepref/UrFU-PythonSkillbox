from csv import DictReader

# Удаляет html теги
def RemoveHTML_Tags(value: str)-> str:
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

# Проверяет, есть ли в csv пустые значения и правильно ли заполнены данные
def ValidateCSV(name: str) -> list:
    fields = list()
    with open(name, encoding='utf-8-sig') as file:
        for row in DictReader(file):
            if row['salary_currency'] != 'RUR' or not all(row.values()):
                continue
 
            fields.append([row['name'],RemoveHTML_Tags(row['employer_name']),row['area_name'],int((float(row['salary_from']) + float(row['salary_to'])) // 2),row['key_skills'].split('\n')])
    return fields

# Склонение
def GetRightFormWord(n: int, first,second,third: str) -> str:
    if n % 10 == 1:
        return first
    if (n % 100 < 11 or n % 100 > 20) and 1 < n % 10 <= 4:
        return second
    return third


# Выводит список самых высоких и низких зарплат
def ListSalaries(l: list)-> None:
    print("Самые высокие зарплаты:")

    l_low = sorted(l, key=lambda x: x[3])
    l_high = sorted(l, key=lambda x: x[3], reverse=True)
    n = 1

    for i in l_high:
        s = GetRightFormWord(i[3],"рубль","рубля","рублей")
        print("    {}) {} в компании \"{}\" - {} {} (г. {})".format(n, i[0], i[1], i[3], s, i[2]))
        n += 1
        if n>10:
            break
    
    print("")
    print("Самые низкие зарплаты:")

    n = 1

    for i in l_low:
        s = GetRightFormWord(i[3],"рубль","рубля","рублей")
        print("    {}) {} в компании \"{}\" - {} {} (г. {})".format(n, i[0], i[1], i[3], s, i[2]))
        n += 1
        if n>10:
            break

# # Выводит список популярных навыков
def ListSkills(l: list) -> None:
    d = dict()
    count = 0

    # Проверка на тип, так как если это не list то, по циклу не надо прогонять
    for field in l:
        if isinstance(field[-1],list):
            for i in field[-1]:
                if i not in d.keys():
                    d[i] = 1
                    count += 1
                else:
                    d[i] += 1
        else:
            if field[-1] not in d.keys():
                d[field[-1]] = 1
                count += 1
            else:
                d[field[-1]] += 1
    
    print("Из {} скиллов, самыми популярными являются:".format(count))

    # d - словарь со скилами и их количеством упоминаний
    d = sorted(d.items(), key=lambda item: item[1], reverse=True)

    n = 1
    for key, value in dict(d).items():
        s = GetRightFormWord(value, "раз","раза","раз")
        print("    {}) {} - упоминается {} {}".format(n, key, value, s))
        n += 1
        if n > 10:
            break

# Выводит список средних зарплат
def ListMediumSalaries(l: list) -> None:
    count_vacancies_cities = {}
 
    for i in l:
        count_vacancies_cities[i[2]] = count_vacancies_cities.get(i[2], []) + [i[3]]
    print(f'Из {len(count_vacancies_cities)} городов, самые высокие средние ЗП:')
    count_vacancies_cities_new = {}
    for key,value in count_vacancies_cities.items():
        if int(len(value) / len(l) * 100) >= 1:
            count_vacancies_cities_new[key] = value
    count_vacancies_cities_new =  sorted(count_vacancies_cities_new.items(), key=lambda x: sum(x[1]) // len(x[1]), reverse=True)
    n = 1
    for i in count_vacancies_cities_new:
        print(f'    {n}) {i[0]} - средняя зарплата {sum(i[1]) // len(i[1])} {GetRightFormWord(sum(i[1]) // len(i[1]), "рубль", "рубля", "рублей")} ({len(i[1])} {GetRightFormWord(len(i[1]), "вакансия", "вакансии", "вакансий")})')
        n+=1
        if n>10:
            break

# Выводит CSV заданному формату в  задание 2.3
def OutputCorrectlyCSV(name: str) -> None:

    l = ValidateCSV(name)
    ListSalaries(l)
    print("")
    ListSkills(l)
    print("")
    ListMediumSalaries(l)


if __name__ == "__main__":
    OutputCorrectlyCSV(input())


