import os
import json
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def clean_text(text):
    """Remove URLs, punctuation, and digits from text and convert to lowercase."""
    pattern = re.compile(r"https?://\S+|[^\w\s]|\d")
    return pattern.sub(" ", text).lower()

def tokenize_and_lemmatize(text):
    """Tokenize and lemmatize the given text."""
    tokens = word_tokenize(text, language='english')
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def remove_stopwords(words):
    """Remove stopwords from a list of words."""
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word not in stop_words]

def clean_and_extract_words(text):
    """Process the given text and extract clean, unique words."""
    cleaned_text = clean_text(text)
    tokens = tokenize_and_lemmatize(cleaned_text)
    filtered_words = remove_stopwords(tokens)
    return set(filtered_words)

def set_default(obj):
    """Custom JSON serialization for sets."""
    if isinstance(obj, set):
        return list(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def preprocess_blog_posts(folder_path):
    """Preprocess all blog posts in the given folder."""
    processed_data = {}
    for filename in filter(lambda f: f.endswith('.json'), os.listdir(folder_path)):
        process_blog_file(os.path.join(folder_path, filename), processed_data)

    save_processed_data(processed_data)

def process_blog_file(file_path, processed_data):
    """Process a single blog file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = json.load(file)
        for entry in content:
            process_blog_entry(entry, file_path, processed_data)

def process_blog_entry(entry, filename, processed_data):
    """Process a single blog entry."""
    entry_text = entry.get('text')
    entry_date = entry.get('date')
    if entry_text and entry_date:
        process_entry_text_and_date(entry_text, entry_date, filename, processed_data)

def process_entry_text_and_date(entry_text, entry_date, filename, processed_data):
    """Process text and date of a blog entry."""
    if isinstance(entry_text, list):
        entry_text = ' '.join(entry_text)
    try:
        year = pd.to_datetime(entry_date).year
        words = clean_and_extract_words(entry_text)
        key = f"{filename}_{year}"
        processed_data.setdefault(key, (filename, year, set())).update(words)
    except ValueError:
        print(f"Unknown date format: {entry_date}")

def save_processed_data(processed_data):
    """Save the preprocessed data to a JSON file."""
    with open('preprocessed_data.json', 'w', encoding='utf-8') as file:
        json.dump(list(processed_data.values()), file, default=set_default)

def preprocess_blogs_and_count_occurrences(folder_path):
    """Main function to preprocess blogs and count word occurrences."""
    preprocess_blog_posts(folder_path)
    # Load and process data as needed...

# Example usage
folder_path = 'test_files'
preprocess_blogs_and_count_occurrences(folder_path)
