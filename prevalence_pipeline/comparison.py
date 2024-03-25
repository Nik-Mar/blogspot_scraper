import pandas as pd
import json


brysbart_file_path = "brysbart_prevalence_files/English_Word_Prevalences.xlsx"
brysbart_results = pd.read_excel(brysbart_file_path, sheet_name="Prevalence")[['Word', 'Pknown']]


for year in range(2004, 2025):
    with open(f'results/{year}.json', 'r', encoding='utf-8') as file:
        year_data = json.load(file)
        year_dfs = pd.DataFrame(year_data.items(), columns=['Word', str(year)])
        brysbart_results = brysbart_results.merge(year_dfs, on='Word', how='left')


brysbart_results.fillna("-", inplace=True)
brysbart_results.to_excel('comparison.xlsx', index=False)
