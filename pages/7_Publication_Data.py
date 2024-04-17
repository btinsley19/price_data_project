# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# st.set_page_config(layout="wide", page_title="Price Data Project", page_icon="✌")

# st.header('USC Price Publication Data', divider='red')
# st.subheader('')

# # Load the data, specifying 'year' column as string data type
# df = pd.read_csv('./data/publications.csv', dtype={'year': str})
# df = df[["name", "title", "year", "citation", "type"]]

# # Remove commas from 'year' column
# df['year'] = df['year'].str.replace(',', '')

# # Convert 'year' column to numeric, handling errors by coercing non-numeric values to NaN
# df['year'] = pd.to_numeric(df['year'], errors='coerce')

# # Remove rows with NaN values in the 'year' column
# df.dropna(subset=['year'], inplace=True)

# # Group by 'year' and aggregate counts of titles and sum of citations
# df_year = df.groupby('year').agg({'title': 'count', 'citation': 'sum'}).reset_index()

# # Create figure and axis objects
# fig, ax1 = plt.subplots()

# # Plot publications over time on the primary y-axis
# ax1.bar(df_year['year'], df_year['title'], color='b', label='Publications')
# ax1.set_xlabel('Year')
# ax1.set_ylabel('Number of Publications', color='b')
# ax1.tick_params('y', colors='b')

# # Create another y-axis for the sum of citations using twinx()
# ax2 = ax1.twinx()
# ax2.plot(df_year['year'], df_year['citation'], color='r', label='Citations')
# ax2.set_ylabel('Sum of Citations', color='r')
# ax2.tick_params('y', colors='r')

# # Add a legend
# fig.tight_layout()
# ax1.legend(loc='upper left')
# ax2.legend(loc='upper right')

# # Show the plot in Streamlit
# st.pyplot(fig)

# st.dataframe(df)