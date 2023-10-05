s = input()
ch = ""
num = ""
f = True

al = "abcdefghijklmnopqrstuvwxyz"

# Добавляем в ch символ
# Проверяем на отрицательность и добавляем в num цифры
for i in s:
    if i == "-":
        f = False
        continue
    if ch == "":
        ch = i
    elif i != ",":
        num += i

num = int(num)

if f == False:
    num = (-1) * num

# Смещение будет происходить правильно при любых num
for i in range(len(al)):
    if al[i] == ch:
        c = (i+num)//len(al)
        if i + num >= len(al)-1:
            print(al[(i+num)-(len(al)*c)])
            break
        if i + num <= 0:
            print(al[(len(al)*(-c))+(i+num)])
            break
        else:
            print(al[i+num])
            break


