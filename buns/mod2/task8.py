s = input()

for i in range(len(s)):
    if s[i] == " ":
        break

s1 = s[:i-1]
ch = s[-1]

count = 0

for i in s1:
    # Идём по строке, пока не встретится символ отличающийся от ch
    if i == ch:
        count += 1
    else:
        break

print(count)