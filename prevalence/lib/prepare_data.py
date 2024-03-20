import pandas as pd

def prepare_data(_loaded_data):
    rows = []  # This will hold the individual words, each as a separate row
    for blog_name, years_words in _loaded_data.items():
        for year, text in years_words.items():
            words = text.split()  # Assume 'text' is a string of words separated by spaces
            for word in words:
                # Append each word as a separate row in the DataFrame
                rows.append({
                    'blog_name': blog_name,
                    'year': int(year),
                    'word': word  # Ensure this is a single word (string), not a list
                })
    return pd.DataFrame(rows)