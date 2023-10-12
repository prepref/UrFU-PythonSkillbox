n = int(input())

res1 = list(list())
res2 = list(list())

for i in range(1,n+1):
    print(", ".join([str(i) for i in range(1,n+1)]))

print('\n')

for i in range(1,n+1):
    print(", ".join([str(i)]*n))
