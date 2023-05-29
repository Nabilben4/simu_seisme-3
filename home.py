import streamlit as st
from PIL import Image
image = Image.open('image/synoptique.png')



st.header("Bienvenue sur le site des :blue[Sciences de l'ingénieur ] du lycée BEAUREGARD")
st.image(image, caption='Synoptique du projet')

st.write("Cette application permet de communiquer avec des capteurs et actionneurs conectés sur un ESP32.")
st.write("La connection en WIFI de cet ESP32 sur un broker :red[MOSQUITTO], permet de transmettre les données via un serveur :yellow[strteamlit]")