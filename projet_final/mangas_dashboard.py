import streamlit as st
import pandas as pd
import requests
from PIL import Image
import os
from os.path import basename

st.set_page_config(layout="wide")

@st.cache
def load_data():
    mangas = requests.get('http://127.0.0.1:5000/mangas').json()["mangas"]
    col = ["ID", "Titre", "Style", "Genre", "Synopsis"]
    mangas = pd.DataFrame(mangas, columns=col)
    return mangas

img = Image.open("C:/Users/diogo/OneDrive/Documents/Ynov/B3/python/projet_final/rank.png")


st.subheader('Mangas collectionnés')
col1, col2, col3 = st.columns([3,6,3])
with col2:
    st.image(img, width=500)

data = load_data()

if st.checkbox('Show dataframe'):
    col1, col2, col3 = st.columns([6,6,6])
    with col2:
        st.dataframe(data['Titre'], width=600, height=900)

st.write("")
img2 = Image.open("C:/Users/diogo/OneDrive/Documents/Ynov/B3/python/projet_final/bib.png")

col1, col2, col3 = st.columns([7,6,7])
with col2:
    st.image(img2, width=300)

manga_list = list(data['Titre'].unique())

col1, col2, col3 = st.columns([6,6,6])
with col2:
    manga = st.selectbox("Choisir un manga :", manga_list)

filtre = data.loc[(data['Titre'] == manga)]

path1 = "C:/Users/diogo/OneDrive/Documents/Ynov/B3/python/projet_final/Death Note.jpg"
fileName, fileExtension1 = os.path.splitext(path1)
Name = fileName.split("/")[-1]

col1, col2, col3 = st.columns([6,6,6])
with col2:
    #image
    if data.iloc[filtre.index]['Titre'].values[0] == Name:
        file = open(fileName + fileExtension1, "rb")
        st.image(file.read(), width=300)
    else:
        st.write("")


#style
col1, col2, col3 = st.columns([6,6,6])
with col2:
    st.write("Style :", data.iloc[filtre.index]['Style'].values[0])

#genre
col1, col2, col3 = st.columns([6,6,6])
with col2:
    st.write("Genre :", data.iloc[filtre.index]['Genre'].values[0])

#synopsis
col1, col2, col3 = st.columns([6,6,6])
with col2:
    st.write("Synopsis :", data.iloc[filtre.index]['Synopsis'].values[0])


path2 = "C:/Users/diogo/OneDrive/Documents/Ynov/B3/python/projet_final/Death Note.mp3"
fileName, fileExtension2 = os.path.splitext(path2)
Name = fileName.split("/")[-1]
#audio
col1, col2, col3 = st.columns([6,6,6])
with col2:
    if data.iloc[filtre.index]['Titre'].values[0] == Name:
        file = open(fileName+fileExtension2, "rb")
        st.audio(file.read())
    else:
        st.write()
