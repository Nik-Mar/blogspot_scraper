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

nlp = spacy.load("en_core_web_sm")



def preprocess(text):
    # preprocessing before NER
    
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub('[0-9]', '', text)
    text=re.sub(r"([!()\[\]])", r" \1 ", text).strip() #'\n'
    text=re.sub(r'\n', '', text)
    nlp.max_length = len(text)+100

    document = nlp(text)
    # recognize named entities

    translator = str.maketrans('', '', string.punctuation) 
    entities_to_keep=['DATE', 'QUANTITY', 'TIME']
    entities_to_remove = [i for i in nlp.get_pipe('ner').labels if not i in entities_to_keep]
    entities = [(ent.text, ent.label_) for ent in document.ents if ent.label_ in entities_to_remove]
    
    pos=[]
    lemmas=[]
    for token in document:
        if not token.is_stop and not token.is_punct and token.is_alpha and not token.ent_type_ in entities_to_remove and token.pos_!="PROPN": #proper noun tag: catches extra things that named entity recognition didnt catch
            #print(token.text, token.pos_, token.lemma_)
            pos.append((token.text, token.pos_))
            lemmas.append(token.lemma_)
    
    return pos, lemmas, set(entities)


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
                    tags=text[0]
                    lemmas=text[1]
                    entities=text[2]
                    result.append({'year': year, 'entities': entities, 'lemmas': lemmas, 'pos': tags})

                output_folder_path=r"C:\Users\Marja\Documents\Projects\Blogspot\prevalence\processed_blogs"
                file_path = os.path.join(output_folder_path, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, default=set_default)


start_time = time.time()
folder_path=r"C:\Users\Marja\Documents\Projects\Blogspot\scraped_blogs"
final_preprocess_blogs(folder_path)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution Time: {elapsed_time:.2f} seconds")


# def combine_preprocessed_lemmas(directory_path):
#     combined_entries = defaultdict(lambda: defaultdict(list))
#     # Iterate through each file in the directory
#     for filename in os.listdir(directory_path):
#         if filename.endswith('.json'):
#             file_path = os.path.join(directory_path, filename)
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 content = json.load(file)
#                 for entry in content:
#                     year = entry.get('year')
#                     lemmas = entry.get('lemmas')
#                     if lemmas and year:
#                         # Join lemmas if it's a list
#                         if isinstance(lemmas, list):
#                             lemmas = ' '.join(lemmas)
#                         # Append the lemmas to the list for the corresponding year and filename
#                         combined_entries[filename][year].append(lemmas)

#     # For each filename and year, join all lemmas into a single string
#     for filename in combined_entries:
#         for year in combined_entries[filename]:
#             combined_entries[filename][year] = ' '.join(combined_entries[filename][year])

#     return dict(combined_entries)
