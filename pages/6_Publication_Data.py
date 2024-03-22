import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Price Data Project", page_icon = "✌")

# st.markdown("""
#     <style>
#     #MainMenu {display: none;}
#     .stDeployButton {display: none;}
#     [data-testid="stHeader"] {background-color: #222222;}
#     .main.st-emotion-cache-uf99v8.ea3mdgi8 {background-color: #222222;}
#     .st-emotion-cache-1dj0hjr{color: #FFC72C;}
#     .st-emotion-cache-1m6wrpk.eczjsme5 {color: #fff;}
#     .st-emotion-cache-6qob1r.eczjsme3 {background-color: #990000;}
    
#     </style>
#     """, unsafe_allow_html=True)

st.header('USC Price Publication Data', divider='red')
st.subheader('')

df = pd.read_csv('./data/articles.csv')
df = df[["name","title", "year", "citation", "type"]]

df_year = df.groupby('year').agg({'title':'count', 'citation':'sum'}).reset_index()

fig, ax1 = plt.subplots()

# Plot publications over time on the primary y-axis
ax1.bar(df_year['year'], df_year['title'], color='b', label='Publications')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Publications', color='b')
ax1.tick_params('y', colors='b')

# Create another y-axis for the sum of citations using twinx()
ax2 = ax1.twinx()
ax2.plot(df_year['year'], df_year['citation'], color='r', label='Citations')
ax2.set_ylabel('Sum of Citations', color='r')
ax2.tick_params('y', colors='r')

# Add a legend
fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Show the plot in Streamlit
st.pyplot(fig)

