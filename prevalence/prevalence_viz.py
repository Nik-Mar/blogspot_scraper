import matplotlib.pyplot as plt
import json
import os
#
# with open('results/2023.json', 'r') as file:
#     data = json.load(file)
#
#
# sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True) # sort it by value in descending order
#
# keys, values = zip(*sorted_data[0:50])  # Select the top n values
#
# plt.figure(figsize=(10, 8))
# plt.bar(keys, values, color='skyblue')
# plt.xlabel('words')
# plt.ylabel('prevalence')
# plt.xticks(rotation=45, ha='right')
# plt.title('Prevalence')
# plt.tight_layout()
# plt.show()




directory = 'results'
word = 'instagram'
years = range(2004, 2025)
values = []

for year in years:
    file_path = os.path.join(directory, f'{year}.json')
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            value = data.get(word, 0)
            values.append(value)
    except FileNotFoundError:
        print(f"File for year {year} not found. Skipping...")
        values.append(0)

# Plotting the line chart
plt.figure(figsize=(10, 6))
plt.plot([str(year) for year in years], values, marker='o', linestyle='-', color='b')
plt.xlabel('Year')
plt.ylabel('Value')
plt.title(f'Prevalence of "{word}" Over Time')
plt.grid(True)
plt.tight_layout()
plt.show()
