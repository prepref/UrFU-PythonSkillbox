import pandas as pd

vacancies = pd.read_csv('vacancies_small.csv')

df = pd.DataFrame(vacancies)
df['salary'] = df[["salary_from", "salary_to"]].sum(axis=1)
df.loc[(((df['salary'] != df['salary_to']) & (df['salary'] == df['salary_from'])) | ((df['salary'] != df['salary_from']) & (df['salary'] == df['salary_to'])))==0,'salary'] = (df['salary_to']+df['salary_from'])/2
gr = df.groupby(['area_name']).agg({'salary':'mean'}).sort_values(by=['salary','area_name'],ascending=(False,True))

salary = gr.to_dict()['salary']

print(salary)
