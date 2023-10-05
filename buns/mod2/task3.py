s= input()
a, b, c = 0, 0, 0
f = True
# f - флаг, который проверяет, является ли число отрицательным
# если мы встретили "-", то вызываем continue, и уже с учетом того,
# что f = False, мы говорим, что перед нами отрицательное число
# после этого присваеваем f = True для проверки следующего числа
for i in s:
    if i == "-":
        f = False
        continue
    if i != " " and a == 0:
        if f:
            a = int(i)
        else:
            a = int(i) * (-1)
            f = True
    elif i != " " and b == 0:
        if f:
            b = int(i)
        else:
            b = int(i) * (-1)
            f = True
    elif i != " " and c == 0:
        if f:
            c = int(i)
        else:
            c = int(i) * (-1)
            f = True

if a>=b and a<=c or a<=b and a>=c:
    print(a)
elif b>=a and b<=c or b<=a and b>=c:
    print(b)
else:
    print(c)

