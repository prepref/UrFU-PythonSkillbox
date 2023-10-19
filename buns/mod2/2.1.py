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

    print(fields_head)
    print(fields)

if __name__ == "__main__":
    OutputCorrectlyCSV(input())


