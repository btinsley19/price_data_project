import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

st.header('USC Price Teaching Analysis', divider='red')
st.subheader('')
st.markdown('''**Note that the majority of teaching data has been excluded -- we are only
            including data regarding full-time faculty at USC Price.''')

data = pd.read_csv('./data/filtered_courses.csv')
data = data[["Course number", "Course title", "Instructor", "Units", "Registered", "Term", "Department"]]
data = data[data['Department'] != 'ROTC']
# Convert 'Units' to numeric, coercing errors
data['Units'] = pd.to_numeric(data['Units'], errors='coerce')
# Optionally, fill NaN values with 0 if you want to treat missing units as 0
data['Units'].fillna(0, inplace=True)
# Function to convert term format after converting integer to string
def convert_term_format(term):
    term_str = str(term)  # Convert the integer to a string
    year = term_str[:4]
    season_code = term_str[-1]
    season = ''
    if season_code == '1':
        season = 'SP'
    elif season_code == '2':
        season = 'SU'
    elif season_code == '3':
        season = 'F'
    return f"{season}{year[2:]}"

# Apply the function to the 'Term' column after converting to string
data['Formatted_Term'] = data['Term'].astype(str).apply(convert_term_format)

selected_terms = st.multiselect('Select Semesters', options=data['Formatted_Term'].unique(), default=data['Formatted_Term'].unique()[0])
filtered_data = data[data['Formatted_Term'].isin(selected_terms)]

# Count unique instructors per department in the filtered data
instructor_counts = filtered_data.groupby('Department')['Instructor'].nunique().reset_index()
instructor_counts.rename(columns={'Instructor': 'Faculty_Count'}, inplace=True)

department_data = filtered_data.groupby('Department').agg(
    Total_Units=('Units', 'sum'),
    Total_Students=('Registered', 'sum'),
    Courses_Taught=('Department', 'count')  # or simply use 'size' function
).reset_index()

department_data = department_data.merge(instructor_counts, on='Department')
department_data['Total_Units_Per_Faculty'] = department_data['Total_Units'] / department_data['Faculty_Count']
department_data['Total_Students_Per_Faculty'] = department_data['Total_Students'] / department_data['Faculty_Count']
department_data['Courses_Taught_Per_Faculty'] = department_data['Courses_Taught'] / department_data['Faculty_Count']

colors = ['#FFC72C', '#990000', 'white']
bar_width = 0.25 

fig, ax = plt.subplots(figsize=(10, 6), facecolor='#222222')  # Set figure background color
ax.set_facecolor('#222222')  # Set axes background color

index = np.arange(len(department_data['Department']))  # Position of groups

# Create bars for each metric
bars1 = ax.bar(index, department_data['Total_Units_Per_Faculty'], bar_width, label='Total Units / Faculty', color=colors[0])
bars2 = ax.bar(index + bar_width, department_data['Total_Students_Per_Faculty'], bar_width, label='Total Students / Faculty', color=colors[1])
bars3 = ax.bar(index + 2 * bar_width, department_data['Courses_Taught_Per_Faculty'], bar_width, label='Courses Taught / Faculty', color=colors[2])

# Function to add value labels on top of each bar with scaled metrics
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',  # Format to 2 decimal places
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, color='white')

# Add labels to each set of bars
add_value_labels(bars1)
add_value_labels(bars2)
add_value_labels(bars3)

new_labels = [f'{dept} \n({count} faculty)' for dept, count in zip(department_data['Department'], department_data['Faculty_Count'])]

ax.tick_params(axis='y', colors='white')  # This should ensure the y-axis labels are white

# Use these new labels in set_xticklabels
ax.set_xticks(index + bar_width)
ax.set_xticklabels(new_labels, rotation=45, ha="right", fontsize=8, color="white")

# Add labels, title, and x-tick labels
ax.set_ylabel('Counts', fontsize=12, color="white")
ax.set_title('Department Metrics by Selected Semesters (Scaled)', fontsize=16, color="white")
# ax.set_xticks(index + bar_width)
# ax.set_xticklabels(department_data['Department'], rotation=45, ha="right", fontsize=8)
legend = ax.legend(facecolor='#222222')
plt.setp(legend.get_texts(), color='white')

# Display the plot
st.pyplot(fig)