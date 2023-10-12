l = list()

while True:
    s = input()
    if s == "":
        break
    else:
        l.append(s)

countX_horizontal = 0
countO_horizontal = 0
countX_vertical = 0
countO_vertical = 0
countX_diagonal1 = 0
countO_diagonal1 = 0
countX_diagonal2 = 0
countO_diagonal2 = 0

# По строкам и двум диагоналям
for i in range(len(l)):
    countX_horizontal = max(countX_horizontal, l[i].count('X'))
    countO_horizontal = max(countO_horizontal, l[i].count('O'))
    if l[i][i] == 'X':
        countX_diagonal1 += 1
    if l[i][i] == 'O':
        countO_diagonal1 += 1
    if l[-i-1][-i-1] == 'X':
        countX_diagonal2 += 1
    if l[-i-1][-i-1] == 'O':
        countO_diagonal2 += 1

# По столбцам
s = ''.join(l)
for i in range(len(l)):
    countX = 0
    countO = 0
    n = 0
    for j in range(i,len(s),len(l)):
        if n == len(l):
            break
        if s[j] == 'X':
            countX += 1
        if s[j] == 'O':
            countO += 1
        n+=1

    countX_vertical = max(countX_vertical,countX)
    countO_vertical = max(countO_vertical,countO)

mX = max(countX_horizontal,countX_vertical,countX_diagonal1,countX_diagonal2)
mO = max(countO_horizontal,countO_vertical,countO_diagonal1,countO_diagonal2)

if mX == len(l):
    print('X')
elif mO == len(l):
    print('O')
else:
    print("Ничья")