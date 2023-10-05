s = input()

numbers = ""

f = True

for i in s:
    if i != " ":
        # Проверяем, если нет такой цифры в numbers, то
        # добавляем туда эту цифру, если есть - выходим из цикла и f = False
        if i not in numbers:
            numbers+=i
        else:
            f = False
            break

print(f)
    

