import re
import csv

file = input()
new_file = input()
highlight = input()
highlight_list = highlight.split(',')

res = list(list())

def RemoveHTML_Tags_ForString(value: str)-> str:
    s = ""
    f = True

    for i in value:
        if i == "<":
            f = False
        if f:
            s += str(i)
        if i == ">":
            f = True

    return s

def Change_DataTime(s: str) -> str:
    l = s.split('T')

    num = '0123456789'
    s_date = ''
    l_date = l[0].split('-')
    for i in range(-1,-len(l_date)-1,-1):
        if i != -len(l_date):
            s_date += l_date[i] + ' '
        else:
            s_date += l_date[i]

    s_time = l[1].replace(':','-')

    return s_time + ' ' + s_date.replace(' ','/')

def ChangeRegister (r,s: str) -> str:
    text = re.findall(r,s,flags=re.IGNORECASE)
    s_new = s
    for j in text:
        s_new = s_new.replace(j, j.upper(),1)
    return s_new

with open(file,'r', encoding="utf8") as f:
    r = csv.reader(f,delimiter=",")
    c = 0
    for row in r:
        if c == 0:
            res.append(row)
        if c > 0:
            s = '@@'.join(row)
            t = re.findall(r'\d{2}[.]\d{2}[^%]', s)
            for i in t:
                s = s.replace(i, i.replace('.',':',1), 1)

            text = re.findall(r'[<].+[>].+[<].+[>]', s)
            for i in text:
                s = s.replace(i, RemoveHTML_Tags_ForString(i), 1)
            
            dt = re.findall(r'\d{4}[-]\d{2}[-]\d{2}[T]\d{2}[:]\d{2}[:]\d{2}[+]\d{4}', s)
            for i in dt:
                s = s.replace(i, Change_DataTime(i),1)

            for i in highlight_list:
                s = ChangeRegister(r'\w*{}\w*'.format(i),s)

            res.append(s.split('@@'))

        c += 1

with open(new_file,'w', encoding="utf8", newline='') as f:
    w = csv.writer(f,delimiter=',')
    w.writerows(res)
