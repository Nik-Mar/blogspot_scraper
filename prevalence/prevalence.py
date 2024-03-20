import pandas as pd
import os
import json
import re
import string
import itertools
from collections import defaultdict
from lib import set_default
from lib import combine_preprocessed_lemmas as cpl
from lib import test_results as tr
from lib import prepare_data as prep



def count_occurrences_vectorized(_df, year):
    # Filter entries by year
    filtered_df = _df[_df['year'] == year]
    # Drop duplicates to ensure each word is counted once per blog
    unique_word_per_blog = filtered_df.drop_duplicates(subset=['blog_name', 'word'])

    # Count how many blogs mention each word
    word_counts = unique_word_per_blog['word'].value_counts()

    # Calculate the total number of blogs that year
    total_blogs = filtered_df['blog_name'].nunique()

    # Calculate the prevalence of each word
    prevalence_map = (word_counts / total_blogs).to_dict()

    print(f"In {year}, there were {total_blogs} blogs and {len(word_counts)} unique lemmas.")

    # Saving the result in a file for the year
    results_directory = "results"
    os.makedirs(results_directory, exist_ok=True)  # Ensure the directory exists
    result_file = f"{year}.json"
    file_path = os.path.join(results_directory, result_file)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(prevalence_map, f, default=set_default)

    return prevalence_map

# directory_path = 'processed_blogs_new'
# combined = cpl.combine_preprocessed_lemmas(directory_path)
# output_folder = "all_blogs_combined.json"
# with open(output_folder, 'w', encoding='utf-8') as f:
#     json.dump(combined, f)
#
#
# with open('all_blogs_combined.json', 'r', encoding='utf-8') as f:
#     loaded_data = json.load(f)
#
# df = prep.prepare_data(loaded_data)
#
# for year in range(2004, 2025):
#     print(year)
#     count_occurrences_vectorized(df, year)



## TEST THE RESULTS
""""
Check the data coming from 'results'
2022:
"thestreet": 0.010638297872340425
"flagship": 0.05319148936170213
"""

with open('all_blogs_combined.json', 'r', encoding='utf-8') as f:
   loaded_data = json.load(f)
selected_year = "2022"
selected_lemma = "thestreet"
a,b = tr.testing_results(loaded_data, selected_year, selected_lemma)
print (f'prevalence is {(len(a) - 2) / len(b)}') #Here I add -2 because year and the word are added to the set as values and we are only interested in the blognames
