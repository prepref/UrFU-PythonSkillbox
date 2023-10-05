num = input()

bin_num = ""
oct_num = ""
hex_num = ""

# Проверяем, является ли целым
for i in num:
    if i == "." or i == ",":
        print("Неверный ввод")
        exit()

num1 = int(num)
num2 = int(num)
num3 = int(num)

# Проверяем, больше ли нуля 
if int(num) < 0:
    print("Неверный ввод")

else:
    # Перевод в двоичную систему
    while num1 > 0:
        bin_num += str(num1%2)
        num1//=2
    # Перевод в восьмеричную систему
    while num2 > 0:
        oct_num += str(num2%8)
        num2//=8
    # Перевод в шестнадцатеричную систему
    while num3 > 0:
        if num3%16 == 10:
            hex_num += "a"
        elif num3%16 == 11:
            hex_num += "b"
        elif num3%16 == 12:
            hex_num += "c"
        elif num3%16 == 13:
            hex_num += "d"
        elif num3%16 == 14:
            hex_num += "e"
        elif num3%16 == 15:
            hex_num += "f"
        else:
            hex_num += str(num3%16)

        num3//=16

print(bin_num[::-1] + " " + oct_num[::-1] + " " + hex_num[::-1])
