import pandas as pd
from collections import Counter

vacancies = pd.read_csv('vacancies_small.csv')

name = input()

df = pd.DataFrame(vacancies)
filtrated_df = df[df['name'].str.lower().str.contains(name.lower(), na=False)]

skills = ';'.join([str(i).replace('\r\n', ';') for i in filtrated_df['key_skills'].to_list()])

cnt = Counter(skills.split(';'))

res = [(key,value) for key,value in cnt.items() if key!='nan']

res.sort(key=lambda x: x[1], reverse=True)

print(res[:5])
