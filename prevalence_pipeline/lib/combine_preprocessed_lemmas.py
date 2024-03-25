from collections import defaultdict
import os
import json

def combine_preprocessed_lemmas(directory_path):
    combined_entries = defaultdict(lambda: defaultdict(list))
    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
                for entry in content:
                    year = entry.get('year')
                    lemmas = entry.get('lemmas')
                    if lemmas and year:
                        # Join lemmas if it's a list
                        if isinstance(lemmas, list):
                            lemmas = ' '.join(lemmas)
                        # Append the lemmas to the list for the corresponding year and filename
                        combined_entries[filename][year].append(lemmas)

    # For each filename and year, join all lemmas into a single string
    for filename in combined_entries:
        for year in combined_entries[filename]:
            combined_entries[filename][year] = ' '.join(combined_entries[filename][year])

    combined_entries = dict(combined_entries)
    return combined_entries