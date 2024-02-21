import matplotlib.pyplot as plt
import json

# Load your data
with open('results/2023.json', 'r') as file:
    data = json.load(file)

# Create a list of (key, value) pairs and sort it by value in descending order
sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

# Unpack the sorted data into two lists: keys and values
keys, values = zip(*sorted_data[:50])  # Select the top 10 values

# Creating the bar chart
plt.figure(figsize=(10, 8))
plt.bar(keys, values, color='skyblue')
plt.xlabel('words')
plt.ylabel('prevalence')
plt.xticks(rotation=45, ha='right')  # Rotate labels to avoid overlap
plt.title('Bar Chart of Keys vs Values')
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
plt.show()


