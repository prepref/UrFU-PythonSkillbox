import pandas as pd

vacancies = pd.read_csv('vacancies_small.csv')

column = input()
key = input()
sort_by = input()

df = pd.DataFrame(vacancies)
filtrated_df = df[df[column].str.lower().str.contains(key.lower(), na=False)]

filtrated_df = filtrated_df.sort_values(by= sort_by, ascending=False)

print(filtrated_df['name'].to_list())