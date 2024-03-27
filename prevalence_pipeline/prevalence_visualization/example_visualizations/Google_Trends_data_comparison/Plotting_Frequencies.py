
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator


data = pd.read_csv('frequency_smartphone.csv')


#x = data['month']
#y = data['smartphone']

# Data is from the US
# Extract year from 'month' column
data['year'] = pd.to_datetime(data['month']).dt.year

# Group data by year and sum the smartphone sales for each year
grouped_data = data.groupby('year')['smartphone'].sum()


plt.plot(list(grouped_data.index), grouped_data.values, marker='o')
plt.xlabel('Year')
plt.ylabel('Relative Frequency Added Up')
plt.title('Google Trends - smartphone')
#plt.gca().xaxis.set_major_locator(YearLocator())
plt.grid(True)
plt.show()


# Read the CSV file
data = pd.read_csv('frequency_smartphone.csv')

# Assuming your CSV has columns named 'x' and 'y'
x = data['month']
y = data['smartphone']

# Plot the data
plt.plot(x, y)
plt.xlabel('Year')
plt.ylabel('Relative Frequency')
plt.title('Google Trends - smartphone')
plt.grid(False)
plt.show()