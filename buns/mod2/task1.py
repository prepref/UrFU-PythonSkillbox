s = input()
a = ""
b = ""

for i in range(len(s)):
    if s[i] == " ":
        break

a = s[:i-1]
b = s[i+1:] 

result = float(a)%float(b)

# Проверяем, является ли результат целым числом,
# чтобы результат соответствовал формату вывода целых чисел
if str(result*10)[-1] == '0':
    print(int(result))
else:
    print(result)