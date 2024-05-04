import pandas as pd
import os
import json
from collections import defaultdict

def prepare_data(_loaded_data):
    rows = []
    for blog_name, years_words in _loaded_data.items():
        for year, text in years_words.items():
            words = text.split()
            for word in words:
                rows.append({
                    'blog_name': blog_name,
                    'word': word  # Remove 'year' key since we don't need it
                })
    return pd.DataFrame(rows)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def combine_preprocessed_lemmas(directory_path):
    combined_entries = defaultdict(lambda: defaultdict(list))
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
                for entry in content:
                    year = entry.get('year')
                    lemmas = entry.get('lemmas')
                    if lemmas and year:
                        if isinstance(lemmas, list):
                            lemmas = ' '.join(lemmas)
                        combined_entries[filename][year].append(lemmas)
    for filename in combined_entries:
        for year in combined_entries[filename]:
            combined_entries[filename][year] = ' '.join(combined_entries[filename][year])
    return dict(combined_entries)

def count_occurrences_overall(_df):
    # Drop duplicates to ensure each word is counted once per blog
    unique_word_per_blog = _df.drop_duplicates(subset=['blog_name', 'word'])

    # Count how many blogs mention each word
    word_counts = unique_word_per_blog['word'].value_counts()

    # Calculate the total number of blogs
    total_blogs = _df['blog_name'].nunique()

    # Calculate the prevalence of each word
    prevalence_map = (word_counts / total_blogs).to_dict()

    print(f"There are {total_blogs} blogs and {len(word_counts)} unique lemmas.")

    # Save the result in a file
    results_directory = "results"
    os.makedirs(results_directory, exist_ok=True)
    result_file = "overall_prevalence.json"
    file_path = os.path.join(results_directory, result_file)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(prevalence_map, f, default=set_default)

    return prevalence_map

directory_path = 'processed_blogs'
combined = combine_preprocessed_lemmas(directory_path)
output_folder = "all_blogs_combined.json"
with open(output_folder, 'w', encoding='utf-8') as f:
    json.dump(combined, f)

with open('all_blogs_combined.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)

df = prepare_data(loaded_data)
count_occurrences_overall(df)


def testing_results(loaded_data,  selected_lemma):
    blogs_containing_word = []
    total_blogs = []
    for blog_name, years_words in loaded_data.items():
        for year, text in years_words.items():
            words = text.split()
            for word in words:
                if word==selected_lemma:
                    total_blogs.append(blog_name)
    return total_blogs

with open('all_blogs_combined.json', 'r', encoding='utf-8') as f:
   loaded_data = json.load(f)
selected_lemma = "colleague"
total_blogs = testing_results(loaded_data, selected_lemma)
unique_set = set(total_blogs)
print(len(unique_set))

