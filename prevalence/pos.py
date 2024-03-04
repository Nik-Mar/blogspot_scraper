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
                if text  is not None:
                        if isinstance(text, list):
                            entry_text = ' '.join(text)
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




# file=
# combined_entries_by_year = combine_entries_by_year(file)

# result=[]
# for year, combined_text in combined_entries_by_year.items():
#     text=preprocess(combined_text)
#     entities=text[0]
#     lemmas=text[1]
#     tags=text[2]
#     result.append({'year': year, 'entities': entities, 'lemmas': lemmas, 'pos': tags})

# start_time = time.time()
# output_file_path =
# with open(output_file_path, 'w') as output_file:
#     json.dump(result, output_file, indent=2)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Execution Time: {elapsed_time:.2f} seconds")

folder_path=r"C:\Users\marja\Documents\Python_Scripts\Blogspot\scraped_blogs"

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


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
            
            output_folder_path=r"C:\Users\marja\Documents\Python_Scripts\Blogspot\processed_blogs"
            file_path = os.path.join(output_folder_path, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, default=set_default)





                    # # Aggregate word counts by year
                    # if year in year_word_counts:
                    #     year_word_counts[year].update(word_count)
                    # else:
                    #     year_word_counts[year] = word_count

# df = pd.DataFrame(year_word_counts)
# csv_file_path = r"C:\Users\marja\Documents\Python_Scripts\Blogspot\crpgaddict_data.csv"
# df.to_csv(csv_file_path)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Execution Time: {elapsed_time:.4f} seconds")

