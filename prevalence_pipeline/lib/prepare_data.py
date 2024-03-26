import pandas as pd

def prepare_data(_loaded_data):
    rows = [] 
    for blog_name, years_words in _loaded_data.items():
        for year, text in years_words.items():
            words = text.split()  
            for word in words:
                rows.append({
                    'blog_name': blog_name,
                    'year': int(year),
                    'word': word  
                })
    return pd.DataFrame(rows)
