import streamlit as st
# import requests
# from bs4 import BeautifulSoup as bs
import pandas as pd

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

st.header('USC Price Data Project', divider='red')
st.subheader('Introduction')
st.markdown('''This is a tool that lets users view publications from USC
            Price faculty. ''')



# url = "https://web-app.usc.edu/ws/soc_archive/soc/term-20233/classes/ppd/"
# response = requests.get(url)
# soup = bs(response.text, 'html.parser')
#
# # Find the link within the div with class 'timestamp'
# link = soup.find('div', class_='timestamp').find('a')
# file_path = []
# # Extract the href attribute value
# if link:
#     link_url = link.get('href')
#     file_path = f'https://web-app.usc.edu/ws/soc_archive/soc/term-20233/classes/ppd/{link_url}'
# else:
#     st.write('Link not found.')
#
# # Send a GET request to the CSV URL
# response = requests.get(file_path)
#
# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Save the CSV content to a file
#     csv_filename = 'data.csv'
#     with open(csv_filename, 'wb') as csv_file:
#         csv_file.write(response.content)
#
#     # Read the CSV file into a Pandas DataFrame
#     df = pd.read_csv(csv_filename)
#
#     # Now you can work with the DataFrame (e.g., display the first few rows)
#     st.dataframe(df.head(), use_container_width=True, height=10000)
#
# else:
#     st.write(f'Error: Failed to download the CSV. Status code: {response.status_code}')
