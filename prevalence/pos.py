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

#Download NLTK resources
nltk.download('words')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def preprocess_text_with_word_count(text):
    # Apply SpaCy NLP pipeline
    doc = nlp(text)
    
    # Extract named entities
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove non-English words
    english_words = set(nltk.corpus.words.words())
    tokens = [token for token in tokens if token.lower() in english_words]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Part-of-speech tagging
    pos_tags = pos_tag(tokens)
    
    # Include named entities in the word count
    word_count = {}
    for word, pos in pos_tags:        if word not in word_count:
            word_count[word] = {pos: 1}
        else:
            if pos not in word_count[word]:
                word_count[word][pos] = 1
            else:
                word_count[word][pos] += 1
    
    # Include named entities in the word count with their respective labels
    for entity, label in named_entities:
        if entity not in word_count:
            word_count[entity] = {'NE_' + label: 1}
        else:
            if 'NE_' + label not in word_count[entity]:
                word_count[entity]['NE_' + label] = 1
            else:
                word_count[entity]['NE_' + label] += 1
    
    return word_count



file="whatever_file"

start_time = time.time()
with open(file, 'r', encoding='utf-8') as file:
        content = json.load(file)
        year_word_counts = {}
        for entry in range(len(content)):
            entry_date = content[entry]['date']
            entry_text = content[entry].get('text') # Using .get() to avoid KeyError if 'text' does not exist
            if entry_text  is not None:
                    if isinstance(entry_text, list):
                        entry_text = ' '.join(entry_text)
                    try:
                        # Attempt to parse the date
                        year = pd.to_datetime(entry_date).year
                    except ValueError:
                        # skip unknown date posts
                         pass
                    #tokenizing, pos, lemm
                    word_count = preprocess_text_with_word_count(entry_text)
                    #print(word_count)
                    # Aggregate word counts by year
                    if year in year_word_counts:
                        year_word_counts[year].update(word_count)
                    else:
                        year_word_counts[year] = word_count
                    
    
df = pd.DataFrame(year_word_counts)
csv_file_path = "yourpath"
df.to_csv(csv_file_path)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution Time: {elapsed_time:.4f} seconds")
print(df.head())
