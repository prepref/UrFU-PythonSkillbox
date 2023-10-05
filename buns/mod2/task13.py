s = input()

sum1 = 0
sum2 = 0

for i in range(len(s)):
    # Если i - четное, то наша цифра стоит на нечетной позиции и наоборот
    if i%2==0:
        sum1+=int(s[i])
    else:
        sum2+=int(s[i])

if (sum1 + sum2*3) % 10 == 0:
    print("yes")
else:
    print("no")
