a = float(input())

p = round(a*4,2)

s = round(a*a,2)

d = round(a*(2**0.5),2)

# Если на вход будет подано целое число, то python после запятой
# поставить только один 0, поэтому я решил использовать format()
print(format(p, '.2f') + ", " + format(s, '.2f') + ", " + str(d))