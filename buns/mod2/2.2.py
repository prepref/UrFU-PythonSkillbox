import csv

# Задание 2.1
# Проверяет, есть ли в строке значения, длина которых равна 0
def ValidateRows(row: list) -> bool:
    for i in row:
        i = " ".join(str(i).split())
        if len(i) == 0:
            return False
    
    return True

# Проверяет, есть ли в csv пустые значения и правильно ли заполнены данные
def ValidateCSV(name: str) -> (list, list):
    fields_head = list()
    fields = list(list())
    with open(name, 'r', encoding="utf-8-sig") as file:
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
def RemoveSpace(fields: list) -> list:
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
def ToList(fields: list) -> list:
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
def CSV_ToDict(fields_head: list, fields: list) -> list:
    new_fields = ToList(fields)
    new_fields = RemoveSpace(new_fields)

    dict_fields = list(dict())

    for field in new_fields:
        d = dict()
        for i in range(len(field)):
            d[fields_head[i]] = field[i]

        dict_fields.append(d)
    
    return dict_fields

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

    # Задание 2.2
    out_as_dict = CSV_ToDict(fields_head,fields)

    for field in range(len(out_as_dict)):
        for key, value in dict(out_as_dict[field]).items():
            s = ""
            if isinstance(value, list):
                for i in value:
                    s += str(i) + ", "
                print(key + ": " + s[:len(s)-2])
                s = ""
            else:
                print(key + ": " + value)

        if len(out_as_dict)-1 != field:
            print('')

if __name__ == "__main__":
    OutputCorrectlyCSV(input())