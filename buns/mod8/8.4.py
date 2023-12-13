import pandas as pd

def to_correct_pd(file_name:str, vac_name:str) -> (pd.DataFrame,pd.DataFrame):
    vacancies = pd.read_csv(file_name)

    df = pd.DataFrame(vacancies)
    df = df[df.salary_currency == "RUR"]
    new_df = df.copy()
    new_df['salary'] = new_df[["salary_from", "salary_to"]].sum(axis=1).fillna(0)
    new_df.loc[(((new_df['salary'] != new_df['salary_to']) & (new_df['salary'] == new_df['salary_from'])) | ((new_df['salary'] != new_df['salary_from']) & (new_df['salary'] == new_df['salary_to'])))==0,'salary'] = (new_df['salary_to']+new_df['salary_from'])/2
    new_df['published_at'] = new_df['published_at'].str.extract(r'(\d{4})').astype(int)
    profession_df = new_df[new_df['name'].str.lower().str.contains(vac_name.lower(), na=False)]
    return new_df, profession_df

def salary_by_year(new_df:pd.DataFrame) -> None:
    res = dict()
    res = new_df.groupby(['published_at']).agg({'salary':'mean'}).astype(int).sort_values(by=['published_at'],ascending=True).to_dict()['salary']
    print(f'Динамика уровня зарплат по годам: {res}')

def number_of_vacancies_by_year(new_df:pd.DataFrame) -> None:
    res = dict()
    res = new_df.groupby(['published_at']).agg({'name':'count'}).sort_values(by=['published_at'],ascending=True).to_dict()['name']
    print(f'Динамика количества вакансий по годам: {res}')

def salary_by_year_profession(new_df: pd.DataFrame, profession_df:pd.DataFrame) -> None:
    res = dict()
    profession_dict = profession_df.groupby(['published_at']).agg({'salary':'mean'}).astype(int).sort_values(by=['published_at'],ascending=True).to_dict()['salary']
    res = new_df.groupby(['published_at']).agg({'salary':'mean'}).astype(int).sort_values(by=['published_at'],ascending=True).to_dict()['salary']
    res_new = dict()
    res_new = {key:profession_dict[key] if key in profession_dict.keys() else 0 for key in res }
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {res_new}')

def number_of_vacancies_by_year_profession(new_df: pd.DataFrame, profession_df:pd.DataFrame) -> None:
    res = dict()
    profession_dict = profession_df.groupby(['published_at']).agg({'name':'count'}).astype(int).sort_values(by=['published_at'],ascending=True).to_dict()['name']
    res = new_df.groupby(['published_at']).agg({'name':'count'}).sort_values(by=['published_at'],ascending=True).to_dict()['name']
    res_new = dict()
    res_new = {key:profession_dict[key] if key in profession_dict.keys() else 0 for key in res }      
    print(f'Динамика количества вакансий по годам для выбранной профессии: {res_new}')

def salary_by_area(profession_df:pd.DataFrame) -> None:
    res = dict()
    df_area_salaries = profession_df.groupby(['area_name']).agg({'salary':'mean', 'name':'count'}).astype(int).sort_values(by=['salary','area_name'],ascending=(False,True))
    df_area_salaries['name'] = df_area_salaries['name']/df_area_salaries['name'].sum()
    df_area_salaries = df_area_salaries[df_area_salaries.name*100 >= 1]             
    res = {key:value for key,value in list(df_area_salaries.to_dict()['salary'].items())[:10]}
    print(f'Уровень зарплат по городам (в порядке убывания): {res}')

def  number_of_vacancies_by_area(profession_df:pd.DataFrame) -> None:
    res = dict()
    df_area_vacancies = profession_df.groupby(['area_name']).agg({'name':'count'}).sort_values(by=['name','area_name'],ascending=(False,True))
    df_area_vacancies['name'] = df_area_vacancies['name']/df_area_vacancies['name'].sum()
    df_area_vacancies = df_area_vacancies[df_area_vacancies.name*100 >= 1]   
    res = {key:round(value,4) for key,value in list(df_area_vacancies.to_dict()['name'].items())[:10]}
    print(f'Доля вакансий по городам (в порядке убывания): {res}')

if __name__ == "__main__":
    file_name = 'vacancies_for_learn.csv'
    vac_name = input()
    new_df, profession_df = to_correct_pd(file_name,vac_name)
    salary_by_year(new_df)
    number_of_vacancies_by_year(new_df)
    salary_by_year_profession(new_df,profession_df)
    number_of_vacancies_by_year_profession(new_df,profession_df)
    salary_by_area(profession_df)
    number_of_vacancies_by_area(profession_df)






