import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#from nltk.tokenize import word_tokenize
import re

# Function to process a single JSON file
def process_file(file_path):
    with open(file_path, 'rb') as file:
        content = json.load(file)
        year_word_counts = {}
        for entry in range(len(content)):
            entry_date = content[entry]['date']
            entry_text = content[entry].get('text')  # Using .get() to avoid KeyError if 'text' does not exist

            if entry_date is not None and entry_text is not None:
                # Check if entry_text is a list and join it into a single string if it is
                if isinstance(entry_text, list):
                    entry_text = ' '.join(entry_text)
                try:
                    # Attempt to parse the date
                    year = pd.to_datetime(entry_date).year

                    # Remove punctuation from text
                    content_punctuation_remove = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?",
                                                        " ", entry_text)
                    word_count = len(content_punctuation_remove.split())

                    # Aggregate word counts by year
                    if year in year_word_counts:
                        year_word_counts[year] += word_count
                    else:
                        year_word_counts[year] = word_count

                except ValueError:
                    # Handle unknown date format
                    print(f"Unknown date format: {entry_date}")
        return year_word_counts

# Iterate over all JSON files
blogs={}
folder_path = r'C:\Users\marja\Documents\Python Scripts\Blogspot\Blogspot\new'
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        year_word_counts = process_file(os.path.join(file_path))
        #blog, year_word_counts = filename, process_file(os.path.join(file_path))
        blogs[filename] = year_word_counts

# Dictionary to a data frame
df = pd.DataFrame(blogs)

# Write df to CSV
csv_file_path = 'word_counts.csv'
df.to_csv(csv_file_path)

"""
# Step 6: Create the Chart
plt.figure(figsize=(15, 8))
sns.heatmap(df, annot=True, fmt="d", cmap='viridis')
plt.title('Total Words by Title and Year')
plt.xlabel('Year')
plt.ylabel('Title')
plt.show()
"""