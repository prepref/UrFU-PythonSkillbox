name = input()
n = 0

f = open(name, 'r')
for line in f:
    n = int(line)

x, y = 0, 0
c = -1

for i in range(n):
    if x > c:
        x -=1
    elif x<0 and x+y == 0:
        c = c-1
        x -= 1
    elif y > c and x==c:
        y -=1
    elif x==c and y==c and x<0:
        c = -c
        x += 1
    elif x==c and y==c and x>0:
        c = -c
        x -= 1
    elif x<c:
        x+=1
    elif y<c and x==c:
        y+=1
    
f.close()

print(x,y)


    
    
     
