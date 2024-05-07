import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# reading the database
data = pd.read_csv("tips.csv")
 
# printing the top 10 rows
st.write("Top 10 Rows:", data.head(10))

## SCATTER PLOT
# Scatter plot with day against tip
plt.scatter(data['day'], data['tip'])
plt.title("Scatter Plot")
plt.xlabel('Day')
plt.ylabel('Tip')
st.pyplot()

# Scatter plot with day against tip and additional size and color
plt.scatter(data['day'], data['tip'], c=data['size'], s=data['total_bill'])
plt.title("Scatter Plot with Size and Color")
plt.xlabel('Day')
plt.ylabel('Tip')
plt.colorbar()
st.pyplot()

# Line plot of tip and size
plt.plot(data['tip'])
plt.plot(data['size'])
plt.title("Line Plot")
plt.xlabel('Index')
plt.ylabel('Value')
st.pyplot()

# Bar chart with day against tip
plt.bar(data['day'], data['tip'])
plt.title("Bar Chart")
plt.xlabel('Day')
plt.ylabel('Tip')
st.pyplot()

# Histogram of total_bills
plt.hist(data['total_bill'])
plt.title("Histogram")
plt.xlabel('Total Bill')
plt.ylabel('Frequency')
st.pyplot()

# Line plot using seaborn
sns.lineplot(x="sex", y="total_bill", data=data)
plt.title('Line Plot using Seaborn')
st.pyplot()

# Scatter plot using seaborn
sns.scatterplot(x='day', y='tip', data=data)
plt.title('Scatter Plot using Seaborn')
st.pyplot()

# Scatter plot using seaborn with hue
sns.scatterplot(x='day', y='tip', data=data, hue='sex')
plt.title('Scatter Plot with Hue using Seaborn')
st.pyplot()

# Line plot using seaborn
sns.lineplot(x='day', y='tip', data=data)
plt.title('Line Plot using Seaborn')
st.pyplot()

# Bar plot using seaborn with hue
sns.barplot(x='day',y='tip', data=data, hue='sex')
plt.title('Bar Plot with Hue using Seaborn')
st.pyplot()

# Histogram using seaborn with hue
sns.histplot(x='total_bill', data=data, kde=True, hue='sex')
plt.title('Histogram with Hue using Seaborn')
st.pyplot()
