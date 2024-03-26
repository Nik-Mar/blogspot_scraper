# Data Science Project
## blogspot_scraping

### Libraries needed
* Scrapy
* time
* datetime
* json

  
After installation and downloading the project, run the scraper like this:
* in command line, navigate to the working directory
* type in "scrapy crawl blogspotspider"
* after it finishes, a json file with blog data should appear in your working directory

* if the file is empty or any of the fields title, text, date, the website most likely has a different structure and css selectors would have to be updated. At the moment the css selectors work for these basic blogspot sites with similar structure

## token_size_per_blog

### Libraries needed
* pandas
* os
* re
* json

token_size.py process JSON files containing blog entries, aggregates word counts by year. Then, it writes the results to a CSV file.

The JSON files processed here are raw blog data, the output of blogspot_scraping.

The output of token_size.py is the csv file named word_counts.csv

Note: The content of "json_files" folder is the same as "scraped_blogs" folder in prevalence_pipeline

### prevalence_pipeline

### Libraries needed
* nltk
* string
* json
* spacy 
* time
* pandas 
* spacy (en_core_web_sm)
* unicodedata
* numpy 
* collections 
* itertools
* re
* os

There are text pre-processing, prevalence calculation and prevalence results comparison steps.
#### 1) Text pre-processing
process_text.py utilizes English language model from spaCy for NLP tasks

Pre-processing includes:
* Removing non-ASCII characters
* Filtering out numbers and punctuation
* Tokenizing text and recognize named entities
* Filtering out stopwords

Output:  
process_text.py writes POS, lemmas, and named entities to a JSON file
entities: Named entities recognized in the text, except dates, quantities, and times
lemmas: Lemmatized forms of the words in the text
pos: POS tags of the words in the text

#### 2) prevalence calculation
To use this script, you should have a directory named 'processed_blogs' with JSON files

Custom Library Functions: It imports custom functions from a lib module, which contains the following:

* set_default: Handles JSON serialization
* combine_preprocessed_lemmas : Combines lemmatized words in 'processed_blogs'
* test_results : Function for validating results manually.
* prepare_data (prep): Processes the output from combine_preprocessed_lemmas and returns "blog_name", "year" and "word(lemma)" in a dataframe

Steps:
1- Drop duplicates to ensure each word is counted once per blog

2- Count how many blogs mention each word

3- Calculate the total number of blogs that year

4- Calculate the prevalence of each word


Output:
lemma-prevalence values are dumped to 21 JSON files correspoding years from 2004 to 2024.

    
#### 3) prevalence comparison
To use this script, you should have a directory named 'results' with JSON files



