import streamlit as st
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

st.header('USC Faculty Search', divider='red')
st.subheader('')

# faculty = pd.read_csv('./data/faculty.csv')
# faculty = faculty[["Name", "Position", "Expertise", "Degree"]]
# publications = pd.read_csv('./data/articles.csv')
# publications = publications[["name","title", "year", "citation", "type"]]
# courses = pd.concat([pd.read_csv("./data/AY23.csv"), pd.read_csv("./data/AY24.csv")], ignore_index=True)
# courses = courses[["Course number", "Course title", "Units", "Registered", "Department", "Term"]]

faculty = pd.read_csv('./data/faculty.csv')
faculty = faculty[["Name", "Position", "Expertise", "Degree"]].reset_index(drop=True)

publications = pd.read_csv('./data/articles.csv')
publications = publications[["name","title", "year", "citation", "type"]].reset_index(drop=True)

courses = pd.read_csv("./data/courses.csv")
courses = courses[["Course number", "Course title", "Instructor", "Units", "Registered", "Term"]].reset_index(drop=True)


# Filter faculty by search term
text_search = st.text_input("Search Faculty", value="")
filtered_faculty = faculty[faculty["Name"].str.contains(text_search, case=False)]
# Display filtered faculty
st.subheader("Matching Faculty")
st.dataframe(
    filtered_faculty,
    # height=700,
    hide_index=True,
)
# st.table(filtered_faculty)

# Display matching publications
st.subheader("Publications by Matching Faculty")
matching_publications = publications[publications["name"].isin(filtered_faculty["Name"])]
st.dataframe(
    matching_publications,
    column_config={
        "year": st.column_config.NumberColumn(
            "Year",
            format="%d",
        ),
    },
    # height=700,
    hide_index=True,
)
# st.table(matching_publications)

# Display matching courses
st.subheader("Courses Taught by Matching Faculty")
matching_courses = courses[courses["Instructor"].isin(filtered_faculty["Name"])]
st.dataframe(
    matching_courses,
    column_config={
        "Term": st.column_config.NumberColumn(
            "Term",
            format="%d",
        ),
    },
    # height=700,
    hide_index=True,
)
# st.table(matching_courses)