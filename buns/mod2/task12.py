s = input()

sym = "()-"

phone_number = ""
phone_number += s[0]

for i in range(1,len(s)):
    # Проверяем есть ли s[i] в sym
    if s[i] not in sym and s[i] != " ":
        phone_number += s[i]

print(phone_number)