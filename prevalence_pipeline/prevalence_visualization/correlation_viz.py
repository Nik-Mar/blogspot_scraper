import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np


with open(r'C:\Users\sebne\Documents\UNI VIE\DA Project\repo\blogspot_scraper\prevalence_pipeline\prevalence_visualization\overall_prevalence.json', 'r') as file:
    data = json.load(file)
overall_prevalence = np.array(list(data.items()), dtype=object)

df = pd.read_excel(r'C:\Users\sebne\Documents\UNI VIE\DA Project\repo\blogspot_scraper\prevalence_pipeline\brysbart_prevalence_files\English_Word_Prevalences.xlsx')
brysbaert = np.array(df)
brysbaert = brysbaert[:,:2]

keys1 = np.array([item[0] for item in overall_prevalence])
values1 = np.array([item[1] for item in overall_prevalence])
keys2 = np.array([item[0] for item in brysbaert])
values2 = np.array([item[1] for item in brysbaert])

# Find common lemmas
common_lemmas = np.intersect1d(keys1, keys2)

# Create dictionaries to map keys to values
value_dict1 = {key: value for key, value in zip(keys1, values1)}
value_dict2 = {key: value for key, value in zip(keys2, values2)}

# Extract the values for the common keys
common_values1 = np.array([value_dict1[key] for key in common_lemmas])
common_values2 = np.array([value_dict2[key] for key in common_lemmas])

# Sort common_values1 for plotting
sorted_indices = np.argsort(common_values1)
sorted_values1 = common_values1[sorted_indices]
sorted_values2 = common_values2[sorted_indices]

# Calculate Pearson's correlation coefficient
correlation_matrix = np.corrcoef(sorted_values1, sorted_values2)
pearson_correlation = correlation_matrix[0, 1]  # Extract the correlation coefficient from the matrix

# Fit a linear line to the sorted data
linear_coefficients = np.polyfit(sorted_values1, sorted_values2, 1)
linear_polynomial = np.poly1d(linear_coefficients)
linear_line_fit = linear_polynomial(sorted_values1)

# Fit a second-degree polynomial to the sorted data
poly_coefficients = np.polyfit(sorted_values1, sorted_values2, 2)
poly_polynomial = np.poly1d(poly_coefficients)
poly_line_fit = poly_polynomial(sorted_values1)

# Create a scatter plot of these values
plt.figure(figsize=(10, 6))
plt.scatter(sorted_values1, sorted_values2, color='blue', marker='o', edgecolors='white', alpha=0.7)
plt.plot(sorted_values1, linear_line_fit, color='red', linestyle='--', label=f'Linear Fit\nPearson\'s r: {pearson_correlation:.2f}')
plt.plot(sorted_values1, poly_line_fit, color='green', linestyle='-', label='2nd-degree Polynomial Fit')
plt.title('Correlation Scatter Plot of Matching Lemmas')
plt.xlabel('Values from our prevalence calculation')
plt.ylabel('Values from Brysbart prevalence calculation')
plt.legend()
plt.grid(True)
plt.show()
