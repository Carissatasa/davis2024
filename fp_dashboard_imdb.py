import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import plotly.express as px
from PIL import Image

# Page title
st.set_page_config(page_title='IMDb Top Picks Movie Explorer', page_icon='🎬', layout="wide",
    initial_sidebar_state="expanded")

# Adding a header image
header_image = Image.open('header2.png')
st.image(header_image, use_column_width=True)

st.title('🎬 IMDb Movie Explorer')

with st.expander('About this app'):
  st.success('by CARISSA RENATASARI, NPM : 21082010041')  
  st.info('This data was taken from the Top Picks page after accessing the movie entitled "La La Land" on June 8, 2024 at 21.34')
  st.warning("**Filtering**\n-  Year range filtering affects Top Grossing Movie Each Year and Runtime of Top Grossing Movie Each Year\n-  Multi-select genres influence Highest Rated Movies, Total Movies Produced by Genre, and Distribution of Movies by Production Company")
  st.markdown("<span style='font-size:20sp; font-weight:bold;'>VISUALIZATION DESCRIPTION</span>", unsafe_allow_html=True)
  st.markdown("<span style='color:green; font-weight:bold;'>Top Grossing Movie Each Year</span>",unsafe_allow_html=True)
  st.write("- **Chart type:** Comparison - Vertical bar chart\n- Displays the highest-grossing movie for each year")
  st.markdown("<span style='color:green; font-weight:bold;'> Runtime of Top Grossing Movie Each Year</span>",unsafe_allow_html=True)
  st.write("- **Chart type:** Comparison - Horizontal bar chart\n- Shows the duration of each movie that has the highest gross for its year. This visualization can be used to analyze whether the duration of a movie affects its gross.")
  st.markdown("<span style='color:green; font-weight:bold;'>Highest Rated Movies by Selected Genre</span>",unsafe_allow_html=True)
  st.write("- **Chart type:** Comparison - Horizontal bar chart\n- Displays movie ratings sorted from highest to lowest based on the selected genres.")
  st.markdown("<span style='color:green; font-weight:bold;'>Total Movies by Genre</span>",unsafe_allow_html=True)
  st.write("- **Chart type:** Composition - Donut chart\n- Shows the number of movies based on the selected genres.")
  st.markdown("<span style='color:green; font-weight:bold;'>Distribution of Movies by Production Company</span>",unsafe_allow_html=True)
  st.write("- **Chart type:** Distribution - Bar histogram\n- Shows the number of movies produced by each production company.")
  st.markdown("<span style='color:green; font-weight:bold;'>The Relationship between Movie Grosses in the United States and Worldwide</span>",unsafe_allow_html=True)
  st.write("- **Chart type:** Relationship - Scatter plot\n- Shows the correlation between a movie's gross in the United States and its gross in worldwide.")

st.subheader('What is the best selling movie rated by its genre and gross?')

# Load data
df = pd.read_csv('imdb_tp_genres.csv')
# Assuming 'release_date' is the column containing the dates in the format '4/8/2022'
df['year'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d').dt.year

#######################
# Main Panel
col1, col2 = st.columns((1.8, 3), gap='medium')

with col1:
  ## Year selection
  year_list = df.year.unique()
  year_selection = st.slider('Select year duration', 1997, 2023, (2011, 2019))
  year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))
  
  df_year_selection = df[df['year'].isin(year_selection_list)]
  
  # Menemukan film terlaris di setiap tahun
  top_gross_per_year = df_year_selection.loc[df_year_selection.groupby('year')['gross_world'].idxmax()]

  # Membentuk DataFrame dengan format yang diinginkan
  reshaped_df = top_gross_per_year[['year', 'title', 'gross_world']].set_index('year')

  # Sort DataFrame berdasarkan tahun secara menurun (descending)
  reshaped_df = reshaped_df.sort_index(ascending=False)
  reshaped_df

  
  # Pre-format gross world values (assuming gross_world is numeric)
  top_gross_per_year['gross_world_millions'] = top_gross_per_year['gross_world'] / 1000000

  # Create the bar chart
  bar_chart = alt.Chart(top_gross_per_year).mark_bar().encode(
      x=alt.X('year:O', title='Year'),
      y=alt.Y('gross_world_millions:Q', title='Gross Earnings (M$)'),  # Use pre-formatted column
      color='title:N',
      tooltip=[alt.Tooltip('title', title='Title'), 'year', alt.Tooltip('gross_world_millions:Q', title='Gross Earnings (M$)')]  # Use pre-formatted column in tooltip
  )

  # Display the chart
  st.markdown('#### Top Grossing Movies Each Year')
  st.altair_chart(bar_chart)

  # Create the bar chart
  bar_chart = alt.Chart(top_gross_per_year).mark_bar().encode(
      y=alt.Y('year:O', title='Year'),
      x=alt.X('runtime_minutes:Q', title='Runtime (minutes)'),
      color='title:N',
      tooltip=[alt.Tooltip('title', title='Title'), 'year', alt.Tooltip('runtime_minutes:Q', title='Runtime (minutes)')]  # Use pre-formatted column in tooltip
    ).properties(
      width='container'
  )

    # Display the chart
  st.markdown('#### Runtime of Top Grossing Movies Each Year')
  st.altair_chart(bar_chart, use_container_width=True)
  

with col2:
  # Input widgets
  ## Genres selection
  genres_list = df.genres.unique()
  genres_selection = st.multiselect('Select genres', genres_list, ['Sci-Fi', 'Action', 'Adventure', 'Thriller', 'Mystery'])

  df_selection = df[df.genres.isin(genres_selection)]

  # Mengambil top 5 film berdasarkan rating untuk genre yang dipilih
  top_5_movies = df_selection.drop_duplicates(subset=['title']).nlargest(5, 'rating')

  # Membuat bar chart horizontal
  st.markdown('#### Highest Rated Movies by Selected Genre')
  chart = alt.Chart(top_5_movies).mark_bar().encode(
      x=alt.X('rating:Q', title='Rating'),
      y=alt.Y('title:N', sort='-x', title='Film Title'),
      color='rating:Q'
  ).properties(
      height=360
  )

  # Menampilkan chart
  st.altair_chart(chart, use_container_width=True)
  
  # Menghitung jumlah film untuk setiap genre yang dipilih
  genre_counts = df_selection['genres'].value_counts().reset_index()
  genre_counts.columns = ['genre', 'count']

  # Membuat pie chart
  st.markdown('#### Total Movies by Genre')
  pie_chart = px.pie(genre_counts, values='count', names='genre', labels={'count':'Number of Films'}, hole=0.3)
  
  # Menampilkan jumlah film pada label
  pie_chart.update_traces(textinfo='label+value', texttemplate='%{label}: %{value}')
  st.plotly_chart(pie_chart, use_container_width=True)

  # Menampilkan histogram
  st.markdown('#### Distribution of Movies by Production Company')
  hist_chart = px.histogram(df_selection, x='production_company', labels={'production_company': 'Production Company'})
  st.plotly_chart(hist_chart, use_container_width=True)
    
  # Scatter plot
  st.markdown('#### The Relationship between Movie Grosses in United States and Worldwide')
  scatter_chart = px.scatter(df, x='gross_us', y='gross_world', color='country_origin')
  st.plotly_chart(scatter_chart, use_container_width=True)
  
