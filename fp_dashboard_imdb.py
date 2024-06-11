import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import plotly.express as px

# Page title
st.set_page_config(page_title='IMDb Top Picks Movie Explorer', page_icon='🎬', layout="wide",
    initial_sidebar_state="expanded")
st.title('🎬 IMDb Movie Explorer')

with st.expander('About this app'):
  st.markdown('**Source**')
  st.info('This data was taken from the Top Picks page after accessing the movie entitled "La La Land" on June 8, 2024 at 21.34')
#   st.markdown('**How to use the app?**')
#   st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')
  
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
  

with col2:
  # Input widgets
  ## Genres selection
  genres_list = df.genres.unique()
  genres_selection = st.multiselect('Select genres', genres_list, ['Sci-Fi', 'Action', 'Adventure', 'Thriller', 'Mystery'])

  df_selection = df[df.genres.isin(genres_selection)]

  # Mengambil top 5 film berdasarkan rating untuk genre yang dipilih
  top_5_movies = df_selection.drop_duplicates(subset=['title']).nlargest(5, 'rating')

  # Membuat bar chart horizontal
  st.markdown('#### Highest Movie Rating by Selected Genre')
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


  # Menampilkan histogram tipe kartu kredit
  st.markdown('#### Production Company Histogram')
  hist_chart = px.histogram(df_selection, x='production_company', labels={'production_company': 'Production Company'})
  st.plotly_chart(hist_chart, use_container_width=True)
    
  # # Scatter plot
  # st.markdown('#### hubungan budget dengan gross world')
  # scatter_chart = px.scatter(df, x='budget', y='gross_world', color='certification')
  # st.plotly_chart(scatter_chart, use_container_width=True) 

  # Scatter plot
  st.markdown('#### The Relationship between Movie Grosses in United States and Worldwide')
  scatter_chart = px.scatter(df, x='gross_us', y='gross_world', color='country_origin')
  st.plotly_chart(scatter_chart, use_container_width=True)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  




