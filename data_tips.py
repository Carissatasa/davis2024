import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as px

# reading the database
data = pd.read_csv("tips.csv")
 
# printing the top 10 rows
# display(data.head(10))

## SCATTER PLOT
# Scatter plot with day against tip
plt.scatter(data['day'], data['tip'])

# Adding Title to the Plot
plt.title("Scatter Plot")

# Setting the X and Y labels
plt.xlabel('Day')
plt.ylabel('Tip')

plt.show()

# Scatter plot with day against tip
plt.scatter(data['day'], data['tip'], c=data['size'], 
            s=data['total_bill'])
 
# Adding Title to the Plot
plt.title("Scatter Plot")
 
# Setting the X and Y labels
plt.xlabel('Day')
plt.ylabel('Tip')
 
plt.colorbar()
 
plt.show()

# Scatter plot with day against tip
plt.plot(data['tip'])
plt.plot(data['size'])
 
# Adding Title to the Plot
plt.title("Scatter Plot")
 
# Setting the X and Y labels
plt.xlabel('Day')
plt.ylabel('Tip')
 
plt.show()

# Bar chart with day against tip
plt.bar(data['day'], data['tip'])
 
plt.title("Bar Chart")
 
# Setting the X and Y labels
plt.xlabel('Day')
plt.ylabel('Tip')
 
# Adding the legends
plt.show()

# histogram of total_bills
plt.hist(data['total_bill'])
 
plt.title("Histogram")
 
# Adding the legends
plt.show()

# draw lineplot
sns.lineplot(x="sex", y="total_bill", data=data)
# setting the title using Matplotlib
plt.title('Title using Matplotlib Function')
plt.show()

sns.scatterplot(x='day', y='tip', data=data,)
plt.show()

sns.scatterplot(x='day', y='tip', data=data,)
plt.show()

sns.scatterplot(x='day', y='tip', data=data,
               hue='sex')
plt.show()

sns.lineplot(x='day', y='tip', data=data)
plt.show()

# using only data attribute
sns.lineplot(data=data.drop(['total_bill'], axis=1))
plt.show()

sns.barplot(x='day',y='tip', data=data, 
            hue='sex')
plt.show()

sns.histplot(x='total_bill', data=data, kde=True, hue='sex')
plt.show()

# plotting the scatter chart
fig = px.scatter(data, x="day", y="tip", color='sex')
# showing the plot
fig.show()

# plotting the scatter chart
fig = px.line(data, y='tip', color='sex')
 
# showing the plot
fig.show()

# plotting the scatter chart
fig = px.bar(data, x='day', y='tip', color='sex')
 
# showing the plot
fig.show()

# plotting the scatter chart
fig = px.histogram(data, x='total_bill', color='sex')
 
# showing the plot
fig.show()
