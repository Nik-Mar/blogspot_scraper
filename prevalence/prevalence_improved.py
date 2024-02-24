import os
import json
import re
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def clean_text(text):
    # Remove URLs, punctuation, and digits from text and convert to lowercase
    pattern = re.compile(r"https?://\S+|[^\w\s]|\d")
    return pattern.sub(" ", text).lower()

def tokenize_and_lemmatize(text):
    # Tokenize and lemmatize the given text
    tokens = word_tokenize(text, language='english')
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def remove_stopwords(words):
    # Remove stopwords from a list of words.
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word not in stop_words]

def clean_and_extract_words(text):
    # Process the given text and extract clean, unique words
    cleaned_text = clean_text(text)
    tokens = tokenize_and_lemmatize(cleaned_text)
    filtered_words = remove_stopwords(tokens)
    return set(filtered_words)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def preprocess_blogs(folder_path):
    preprocess_data = {}  # List to hold (filename, year, set of words) tuples

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            print(filename)
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
                for entry in content:
                    entry_text = entry.get('text')
                    entry_date = entry.get('date')
                    if entry_text and entry_date:
                        if isinstance(entry_text, list):
                            entry_text = ' '.join(entry_text)
                        try:
                            year = pd.to_datetime(entry_date).year
                            words = clean_and_extract_words(entry_text)
                            key = filename + "_" + str(year)
                            if key in preprocess_data:
                                preprocess_data[key][2].update(words)
                            else:
                                preprocess_data[key] = (filename, year, words)
                        except ValueError:
                            print(f"Unknown date format: {entry_date}")

    value_list = list(preprocess_data.values())

    # Save preprocessed data
    with open('preprocessed_data.json', 'w', encoding='utf-8') as f:
        json.dump(value_list, f, default=set_default)


def create_master_set(_data):
    master_set = set()
    for words in _data:
        master_set.update(words)
    return master_set


def count_occurrences(_loaded_data, year):
    # Filter for blog posts of a given year
    filtered_data = list()
    for entry in _loaded_data:
        if entry[1] == year:
            filtered_data.append(entry[2])

    # Creating master of a given year
    master_set_of_year = create_master_set(filtered_data)

    # Calculating prevalence and saving it in dict
    prevalence_map = dict()
    author_count = len(filtered_data)
    print(f"In {year} there were {author_count} blog authors and {len(master_set_of_year)} unique words.")
    for master_word in master_set_of_year:
        count = 0
        for entry in filtered_data:
            if master_word in entry:
                count += 1
        prevalence = count / author_count
        prevalence_map[master_word] = prevalence
        #print("One word done")

    print("Prevalence calculation done")
    # Saving the result in a file for the year
    result_file = f"{year}.json"
    file = os.path.join("results", result_file)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(prevalence_map, f, default=set_default)
    return prevalence_map


#folder_path = 'json_files'
#preprocess_blogs(folder_path)


with open('preprocessed_data.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)

for year in range(2004, 2025):
    count_occurrences(loaded_data, year)


# k = Counter(prev)
# print(k.most_common(100))
# word = "the"
# print(f"{word} has {prev[word]}")
