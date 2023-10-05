s = input()

count0 = 0
count1 = 0

for i in s:
    if int(i) == 0:
        count0 += 1
    else:
        count1 += 1

if count1 == count0:
    print("yes")
else:
    print("no")
