# USC Price Data Project

The Price Data Project is a joint effort between myself (Brian Tinsley) and Professor Alice Chen with USC Price.
This collaborative project aims to create a centralized hub for accessing faculty publications and course data relevant to students, faculty, and administrators.
It is still a work in progress and big updates can be expected by Fall 2024.


## Overview and File Structure
This repository contains webscraping code for collecting data and a streamlit application that displays USC Price data.
The publication data is from the Google Scholar profiles of USC Price faculty, and the course data is from the USC classes website.

To view the data, you can navigate to the "data" folder.
The *faculty.csv* contains biographical information about USC Price full-time faculty.
The *courses_final.csv* contains all of the USC Price courses offered since 2017.
The *publications.csv* contains simplified data relating to all publications from USC Price faculty.
To see the more detailed data for publications, go to the webscraping/scholars directory and view the aritcles_final.json file.

Inside the webscraping folder, you will find one folder for each of the python scraping scripts (courses, faculty, scholars).
These python notebooks are commented throughout and are explained in more depth in my implementation video.

Note that you will be unable to run these scripts since I removed my secret client ID for my ZenRows account (for proxies); 
it would be irresponsible to leave it out there on the web and people could run up my usage and cost me lots of $.

Home.py is the home page of the streamlit application, and the pages folder contains the other pages which you see on the sidebar of the app interface.

The CRUD page on the application directly interacts with the MongoDB databases which store all of the publication data.
On this page, you can create, read, update, and delete publications directly from the database.
This page is password protected but the password is: pricedataproject

The requirements.txt file contains the 3 required dependencies for running the streamlit application: streamlit, pymongo, and matplotlib.

The .streamlit directory contains the configuration file which determines the design of the streamlit app.


## Running the application

Make sure you have python and pip installed on your machine, then follow these steps

git clone https://github.com/btinsley19/price_data_project.git
cd price_data_project
pip install -r requirements.txt
streamlit run home.py

A Streamlit webapp will run on your local host and you can explore 