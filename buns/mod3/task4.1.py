import json
import re

text = input()
headings = input()

text = text[:len(text)-1]

s1_list = text.split(";")
s2_list = headings.split(",")

for i in range(len(s1_list)):
    s1_list[i] = s1_list[i].strip()

for i in range(len(s2_list)):
    s2_list[i] = s2_list[i].strip()

def Description(s: str) -> str:
    s_list = s.split(". ")
    s_new = ""
    for i in range(len(s_list)):
        s_list[i] = s_list[i].lower()

        a = s_list[i][0]
        a= a.upper()
        s_list[i] = a + s_list[i][1:]

        if i != len(s_list) - 1:
            s_new += s_list[i] + ". "
        else:
            s_new += s_list[i]
    
    return s_new

def Salary(num: float) -> str:
    return format(round(num, 3), '.3f')

def Key_phrase(s: str) -> str:
    return s.upper() + '!'

def Addition(s: str) -> str:
    return '...' + s.lower() + '...'

def Reverse(s: str) -> str:
    return "".join(reversed(s))

def Company_info(s: str) -> str:
    c = 0
    s_new = ""
    for i in range(len(s)):
        if s[i] == '(':
            c+=1
        if c==0:
            s_new += s[i]
        if s[i] == ')':
            c-=1
    
    return s_new


def Key_skills(s: str) -> str:
    return s.replace("&nbsp", " ")

d = dict()

for i in range(len(s1_list)):
    l = s1_list[i].split(": ")
    d[l[0]] = l[1]

d_result = dict()

for i in range(len(s2_list)):
    if s2_list[i] in d.keys():
        if s2_list[i] == "description":
            d_result[s2_list[i]] = Description(d[s2_list[i]])
        elif s2_list[i] == "salary":
            d_result[s2_list[i]] = Salary(float(d[s2_list[i]]))
        elif s2_list[i] == "key_phrase":
            d_result[s2_list[i]] = Key_phrase(d[s2_list[i]])
        elif s2_list[i] == "addition":
            d_result[s2_list[i]] = Addition(d[s2_list[i]])
        elif s2_list[i] == "reverse":
            d_result[s2_list[i]] = Reverse(d[s2_list[i]])
        elif s2_list[i] == "company_info":
            d_result[s2_list[i]] = Company_info(d[s2_list[i]])
        elif s2_list[i] == "key_skills":
            d_result[s2_list[i]] = Key_skills(d[s2_list[i]])


result = json.dumps(d_result)

print(result)