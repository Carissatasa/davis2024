import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.header("Hai!")
st.write("Ini hasil deploy data TIPS di Streamlit")
st.write("Nama : Carissa Renatasari \n NPM : 21082010041")

# reading the database
data = pd.read_csv("tips.csv")
 
# printing the top 10 rows
st.write("Top 10 Rows:", data.head(10))

## SCATTER PLOT
# Scatter plot with day against tip
fig, ax = plt.subplots()
ax.scatter(data['day'], data['tip'])
ax.set_title("Scatter Plot")
ax.set_xlabel('Day')
ax.set_ylabel('Tip')
st.pyplot(fig)

# Scatter plot with day against tip and additional size and color
fig, ax = plt.subplots()
ax.scatter(data['day'], data['tip'], c=data['size'], s=data['total_bill'])
ax.set_title("Scatter Plot with Size and Color")
ax.set_xlabel('Day')
ax.set_ylabel('Tip')
fig.colorbar(ax.collections[0], ax=ax)
st.pyplot(fig)

# Line plot of tip and size
fig, ax = plt.subplots()
ax.plot(data['tip'], label='Tip')
ax.plot(data['size'], label='Size')
ax.set_title("Line Plot")
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.legend()
st.pyplot(fig)

# Bar chart with day against tip
fig, ax = plt.subplots()
ax.bar(data['day'], data['tip'])
ax.set_title("Bar Chart")
ax.set_xlabel('Day')
ax.set_ylabel('Tip')
st.pyplot(fig)

# Histogram of total_bills
fig, ax = plt.subplots()
ax.hist(data['total_bill'])
ax.set_title("Histogram")
ax.set_xlabel('Total Bill')
ax.set_ylabel('Frequency')
st.pyplot(fig)

# Line plot using seaborn
fig, ax = plt.subplots()
sns.lineplot(x="sex", y="total_bill", data=data, ax=ax)
ax.set_title('Line Plot using Seaborn')
st.pyplot(fig)

# Scatter plot using seaborn
fig, ax = plt.subplots()
sns.scatterplot(x='day', y='tip', data=data, ax=ax)
ax.set_title('Scatter Plot using Seaborn')
st.pyplot(fig)

# Scatter plot using seaborn with hue
fig, ax = plt.subplots()
sns.scatterplot(x='day', y='tip', data=data, hue='sex', ax=ax)
ax.set_title('Scatter Plot with Hue using Seaborn')
st.pyplot(fig)

# Line plot using seaborn
fig, ax = plt.subplots()
sns.lineplot(x='day', y='tip', data=data, ax=ax)
ax.set_title('Line Plot using Seaborn')
st.pyplot(fig)

# Bar plot using seaborn with hue
fig, ax = plt.subplots()
sns.barplot(x='day',y='tip', data=data, hue='sex', ax=ax)
ax.set_title('Bar Plot with Hue using Seaborn')
st.pyplot(fig)

# Histogram using seaborn with hue
fig, ax = plt.subplots()
sns.histplot(x='total_bill', data=data, kde=True, hue='sex', ax=ax)
ax.set_title('Histogram with Hue using Seaborn')
st.pyplot(fig)
