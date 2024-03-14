import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import string
import json
import spacy 
import time
import pandas as pd
nlp = spacy.load("en_core_web_sm")
from spacy.pipeline.ner import EntityRecognizer
import unicodedata
import numpy as np
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from nltk import FreqDist
import itertools
import re
import os
from nltk.corpus import wordnet
from collections import defaultdict


#Download NLTK resources
# nltk.download('words')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    elif  pos_tag.startswith('M'):
        return wordnet.VERB   
    elif  pos_tag.startswith('I'):
        return wordnet.ADV
    else:
        return None  # Default to noun if no specific POS tag is found

def lemmatize_pos_tokens(pos_tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = []

    for token, pos_tag in pos_tokens:
        pos = get_wordnet_pos(pos_tag)
        if pos is None:# not supply tag in case of None
            lemma = lemmatizer.lemmatize(token) #unknown word?
        else:
            lemma = lemmatizer.lemmatize(token, pos=pos)     
        lemmatized_tokens.append(lemma)

    return lemmatized_tokens


def preprocess(text):

    # preprocessing before NER
    
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'\d', '', text)
    text=re.sub(r"([!()\[\]])", r" \1 ", text)

    document = nlp(text)

    # recognize named entities
    entities = [(ent.text, ent.label_) for ent in document.ents if ent.label_ not in ["DATE", "TIME", "QUANTITY"]]

    #text without entities
    text_without_ne = [token.text for token in document if token.ent_type_ not in ['GPE', 'PERSON', 'ORDINAL', 'CARDINAL', 'ORG', 'LOC', 'FAC', 'NORP', 'EVENT', 'LAW', 'WORK_OF_ART', 'NER', 'PRODUCT']]
    text=(" ".join(text_without_ne))

    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)

    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.lower() not in stop_words] #stop words
    tokens= [token for token in tokens if len(token) > 1] #one character tokens
    
    #removing cardinals becaue NER doesn't always recognize them
    cardinal_strings = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
    tokens = [token for token in tokens if token.lower() not in cardinal_strings]

    pos_tags = pos_tag(tokens)

    wntags = [(word.lower(), get_wordnet_pos(pos)) for word, pos in pos_tags]

    lemmatized_tokens = lemmatize_pos_tokens(pos_tags)
    lemmatized_tokens = [token.lower() for token in lemmatized_tokens]

    return entities, lemmatized_tokens, wntags


def combine_entries_by_year(path):
    with open(path, 'r', encoding='utf-8') as file:
            content = json.load(file)
            entries_by_year = defaultdict(list)
            for entry in range(len(content)):
                date_= content[entry]['date']
                text = content[entry].get('text')
                if text and date_ is not None:
                        if isinstance(text, list):
                            text = ' '.join(text)
                        try:
                            # Attempt to parse the date
                            year = pd.to_datetime(date_).year
                        except ValueError:
                            # skip unknown date posts
                            pass
                        if year is not None:
                            entries_by_year[year].append(text)
                        
            combined_entries = {}
            for year, text_list in entries_by_year.items():
                combined_entries[year] = ' '.join(text_list)

    return combined_entries           


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def final_preprocess_blogs(folder_path):
    start_time = time.time()
    for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                print(filename)
                file_path = os.path.join(folder_path, filename)
                combined_entries_by_year = combine_entries_by_year(file_path)

                result=[]
                for year, combined_text in combined_entries_by_year.items():
                    text=preprocess(combined_text)
                    entities=text[0]
                    lemmas=text[1]
                    tags=text[2]
                    result.append({'year': year, 'entities': entities, 'lemmas': lemmas, 'pos': tags})

                output_folder_path="processed_blogs"
                file_path = os.path.join(output_folder_path, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, default=set_default)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution Time: {elapsed_time:.2f} seconds")


#nlp.max_length = 1800000
#folder_path='scraped_blogs'
#final_preprocess_blogs(folder_path)



def find_low_freq_lemma(folder_path):
    """
    Here we find the lemmas occur at most twice in a year and create a json file
    which includes a nested dictionary of year-lemma-count data
    """
    # The dictionary maps years to dictionaries, which map lemmas to their counts
    lemmas_frequency_per_year = defaultdict(lambda: defaultdict(int))

    def lemma_counter(folder_path):
        try:
            for filename in os.listdir(folder_path):
                if filename.endswith('.json'):
                    print(filename)
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    # Increment the count for each lemma in the respective year
                    for record in data:
                        year = record['year']
                        for lemma in record['lemmas']:
                            lemmas_frequency_per_year[year][lemma] += 1
        except FileNotFoundError:
            print(f"File not found.")


    lemma_counter(folder_path)

    # Keep only lemmas that occur at most twice in each year
    filtered_lemmas_per_year = {}
    for year, lemmas in lemmas_frequency_per_year.items():
        filtered_lemmas = {lemma: count for lemma, count in lemmas.items() if count <= 2}
        filtered_lemmas_per_year[year] = filtered_lemmas

    # Dump the low freq lemmas into a JSON file
    output_folder="low_freq_lemmas.json"
    with open(output_folder, 'w', encoding='utf-8') as f:
        json.dump(filtered_lemmas_per_year, f, default=set_default)



#folder_path = 'processed_blogs'
#find_low_freq_lemma(folder_path)



def create_master_set(_data):
    """
    Create the set of all lemmas in the corpus
    """
    master_set = set()
    for words in _data:
        master_set.update(words)
    return master_set


def create_master_set(data):
    master_set = set()
    for words in data:
        master_set.update(words.split())
    return master_set


def count_occurrences(_loaded_data, year):
    """
    Prevalence calculation
    """
    filtered_data = []

    # Adjusting to the new structure
    for filename, years_data in _loaded_data.items():
        text = years_data.get(str(year))
        if text:
            filtered_data.append(text)

    # Creating master set of a given year
    master_set_of_year = create_master_set(filtered_data)

    # Calculating prevalence
    prevalence_map = dict()
    author_count = len(filtered_data)
    print(f"In {year} there were {author_count} blog authors and {len(master_set_of_year)} unique lemmas.")

    word_counts = Counter(" ".join(filtered_data).split())

    for word in master_set_of_year:
        prevalence = word_counts[word] / author_count
        prevalence_map[word] = prevalence

    print("Prevalence calculation done")

    # Saving the result in a file for the year
    results_directory = "results"
    os.makedirs(results_directory, exist_ok=True)  # Ensure the directory exists
    result_file = f"{year}.json"
    file_path = os.path.join(results_directory, result_file)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(prevalence_map, f, default=set_default)

    return prevalence_map


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

    return dict(combined_entries)


directory_path = 'processed_blogs'
combined = combine_preprocessed_lemmas(directory_path)
output_folder = "combined.json"
with open(output_folder, 'w', encoding='utf-8') as f:
    json.dump(combined, f)


with open('combined.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)

for year in range(2004, 2025):
    count_occurrences(loaded_data, year)
