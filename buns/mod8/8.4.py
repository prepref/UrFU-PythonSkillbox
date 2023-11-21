import pandas as pd

file_name = 'vacancies_for_learn_demo.csv'
vac_name = input()

vacancies = pd.read_csv(file_name)

df = pd.DataFrame(vacancies)
new_df = df.copy()
new_df['salary'] = new_df[["salary_from", "salary_to"]].sum(axis=1).fillna(0)
new_df.loc[(((new_df['salary'] != new_df['salary_to']) & (new_df['salary'] == new_df['salary_from'])) | ((new_df['salary'] != new_df['salary_from']) & (new_df['salary'] == new_df['salary_to'])))==0,'salary'] = (new_df['salary_to']+new_df['salary_from'])/2
new_df['published_at'] = new_df['published_at'].str.extract(r'(\d{4})').astype(int)

res = dict()

profession_df = new_df[new_df['name'].str.lower().str.contains(vac_name.lower(), na=False)]

res = new_df.groupby(['published_at']).agg({'salary':'mean'}).astype(int).sort_values(by=['published_at'],ascending=True).to_dict()['salary']
print(f'Динамика уровня зарплат по годам: {res}')

res = new_df.groupby(['published_at']).agg({'name':'count'}).sort_values(by=['published_at'],ascending=True).to_dict()['name']
print(f'Динамика количества вакансий по годам: {res}')

profession_dict = profession_df.groupby(['published_at']).agg({'salary':'mean'}).astype(int).sort_values(by=['published_at'],ascending=True).to_dict()['salary']
res = new_df.groupby(['published_at']).agg({'salary':'mean'}).astype(int).sort_values(by=['published_at'],ascending=True).to_dict()['salary']
res_new = dict()

for key in res:
    if key in profession_dict.keys():
        res_new[key] = profession_dict[key]
    else:
        res_new[key] = 0

print(f'Динамика уровня зарплат по годам для выбранной профессии: {res_new}')

profession_dict = profession_df.groupby(['published_at']).agg({'name':'count'}).astype(int).sort_values(by=['published_at'],ascending=True).to_dict()['name']
res = new_df.groupby(['published_at']).agg({'name':'count'}).sort_values(by=['published_at'],ascending=True).to_dict()['name']
res_new = dict()

for key in res:
    if key in profession_dict.keys():
        res_new[key] = profession_dict[key]
    else:
        res_new[key] = 0
        
print(f'Динамика количества вакансий по годам для выбранной профессии: {res_new}')
 
df_area_salaries = profession_df.groupby(['area_name']).agg({'salary':'mean', 'name':'count'}).astype(int).sort_values(by=['salary','area_name'],ascending=(False,True))
df_area_salaries['name'] = df_area_salaries['name']/df_area_salaries['name'].sum()
df_area_salaries = df_area_salaries[df_area_salaries.name*100 >= 1]             
res = {key:value for key,value in list(df_area_salaries.to_dict()['salary'].items())[:10]}
print(f'Уровень зарплат по городам (в порядке убывания): {res}')

df_area_vacancies = profession_df.groupby(['area_name']).agg({'name':'count'}).sort_values(by=['name','area_name'],ascending=(False,True))
df_area_vacancies['name'] = df_area_vacancies['name']/df_area_vacancies['name'].sum()
df_area_vacancies = df_area_vacancies[df_area_vacancies.name*100 >= 1]   
res = {key:round(value,4) for key,value in list(df_area_vacancies.to_dict()['name'].items())[:10]}
print(f'Доля вакансий по городам (в порядке убывания): {res}')











