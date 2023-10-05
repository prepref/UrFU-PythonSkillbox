s = input()

al = "уеёаоыэияю"

count1 = 0
count2 = 0

for i in s:
    # Проверяем находится ли символ в строке al
    if i in al:
        count1 += 1
    elif i != " ":
        count2 += 1

print(count1, count2)