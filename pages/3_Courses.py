import streamlit as st
import pandas as pd
st.set_page_config(layout="wide", page_title="Price Data Project", page_icon = "✌")

st.markdown("""
    <style>
    #MainMenu {display: none;}
    .stDeployButton {display: none;}
    [data-testid="stHeader"] {background-color: #222222;}
    .main.st-emotion-cache-uf99v8.ea3mdgi8 {background-color: #222222;}
    .st-emotion-cache-1dj0hjr{color: #FFC72C;}
    .st-emotion-cache-1m6wrpk.eczjsme5 {color: #fff;}
    .st-emotion-cache-6qob1r.eczjsme3 {background-color: #990000;}
    </style>
    """, unsafe_allow_html=True)

st.header('USC Price Classes Offered', divider='red')
st.subheader('')

combined_df = pd.read_csv("./data/courses.csv")
data = combined_df[["Course number", "Course title", "Instructor", "Units", "Registered", "Term"]]
st.dataframe(
    data,
    column_config={
        "Term": st.column_config.NumberColumn(
            "Term",
            format="%d",
        ),
    },
    height=700,
    hide_index=True,
)