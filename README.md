# Data Science Project
## [Blogspot Scraping Process]

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

## [Token size per blog]

### Libraries needed
* pandas
* os
* re
* json

token_size.py process JSON files containing blog entries, aggregates word counts by year. Then, it writes the results to a CSV file.

The JSON files processed here are raw blog data, the output of blogspot_scraping.

The output of token_size.py is the csv file named word_counts.csv

Note: The content of "json_files" folder is the same as "scraped_blogs" folder in prevalence_pipeline

## [Prevalence pipeline]



There are text pre-processing, prevalence calculation and prevalence results comparison steps.

#### 1) [Text pre-processing]

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

#### 2) [Prevalence calculation]

### Libraries needed
* string
* json 
* pandas 
* collections 
* itertools
* re
* os
  
To use prevalence.py, you should have a directory named 'processed_blogs' with JSON files

Custom Library Functions: It imports custom functions from a lib module, which contains the following:

* set_default: Handles JSON serialization
* combine_preprocessed_lemmas : Combines lemmatized words in 'processed_blogs'
* test_results : Function for validating results manually.
* prepare_data (prep): Processes the output from combine_preprocessed_lemmas and returns "blog_name", "year" and "word(lemma)" in a dataframe

Steps:
1- Drop duplicates to ensure each word is counted once per blog

2- Count how many blogs mention each word

3- Calculate the total number of blogs which were active that year

4- Calculate the prevalence of each word

One can validate prevalence results of specific year-lemma combination using testing_results function.

Output:
lemma-prevalence values are dumped to 21 JSON files correspoding years from 2004 to 2024.

    
#### 3) [Prevalence comparison]

### Libraries needed
* json
* pandas 

To use this script, you should have a directory named 'results' with JSON files.

It merges the project output prevalence values into the  Brysbart's prevalence data (Pknown value) by as a left join. 

Output:
An .xlsx file which contains Brysbart's set of words, Pknown value and our prevalence values for corresponding word. Each column represents the year.

### [Prevalence visualization]

### Libraries needed
* matplotlib
* json
* os
 
prevalence_viz.py returns a bar chart showing the word prevalences in a specific year in descending order, and a line chart of prevalence values of a selected word over years. 
There are example line charts in example_visualizations folder.


[Text pre-processing]: [http://www.reddit.com](https://github.com/Nik-Mar/blogspot_scraper/blob/main/prevalence_pipeline/process_text.py)https://github.com/Nik-Mar/blogspot_scraper/blob/main/prevalence_pipeline/process_text.py]
[Prevalence calculation]: [https://github.com/Nik-Mar/blogspot_scraper/blob/main/prevalence_pipeline/prevalence.py]
[Prevalence comparison]: [https://github.com/Nik-Mar/blogspot_scraper/blob/main/prevalence_pipeline/comparison.py]
[Prevalence visualization]: [https://github.com/Nik-Mar/blogspot_scraper/tree/main/prevalence_pipeline/prevalence_visualization]
[Blogspot Scraping Process]: [https://github.com/Nik-Mar/blogspot_scraper/tree/main/Blogspot_scraping]
[Token size per blog]: [https://github.com/Nik-Mar/blogspot_scraper/tree/main/token_size_per_blog]
[Prevalence pipeline]: [https://github.com/Nik-Mar/blogspot_scraper/tree/main/prevalence_pipeline]
