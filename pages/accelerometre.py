import streamlit as st
import plotly.graph_objects as go
import paho.mqtt.client as mqtt
import sqlite3
import time






#------------configuration du broker et des topics ------------------------
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic1 = "test/gyro_x"
mqtt_topic2 = "test/gyro_y"
mqtt_topic3 = "test/gyro_z"
mqtt_topic4 = "test/accel_x"
mqtt_topic5 = "test/accel_y"
mqtt_topic6 = "test/accel_z"
mqtt_topic7 = "test/temp"

#------------connexion au broker ------------------------------------
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker, mqtt_port)

#------------souscription aux différents topics--------------------------
#----3 pour le gyroscope
#----3 pour l'accélérometre 
#----1 pour la température
mqtt_client.subscribe(mqtt_topic1)
mqtt_client.subscribe(mqtt_topic2)
mqtt_client.subscribe(mqtt_topic3)
mqtt_client.subscribe(mqtt_topic4)
mqtt_client.subscribe(mqtt_topic5)
mqtt_client.subscribe(mqtt_topic6)
mqtt_client.subscribe(mqtt_topic7)

#-------initialisation des listes dans lesquelles seront sauvegardé les données---
gyro_x=[]
gyro_y=[]
gyro_z=[]
accel_x= []
accel_y= []
accel_z= []
temp=[]

# fonction permettant de recevoir les messages et de les stocker
def on_message(client,userdata,message):
    

#-------réception des messages et enregistrements-----------
    if message.topic == mqtt_topic1 :
        new_data = message.payload.decode("utf-8")
        gyro_x.append(float(new_data))

    
    if message.topic == mqtt_topic2 :
        new_data = message.payload.decode("utf-8")
        gyro_y.append(float(new_data))

    if message.topic == mqtt_topic3 :
        new_data = message.payload.decode("utf-8")
        gyro_z.append(float(new_data))

    if message.topic == mqtt_topic4 :
        new_data = message.payload.decode("utf-8")
        accel_x.append(float(new_data))
    
    if message.topic == mqtt_topic5 :
        new_data = message.payload.decode("utf-8")
        accel_y.append(float(new_data))

    if message.topic == mqtt_topic6 :
        new_data = message.payload.decode("utf-8")
        accel_z.append(float(new_data))
    
    if message.topic == mqtt_topic7 :
        new_data = message.payload.decode("utf-8")
        temp.append(float(new_data))
 
st.title("Exemple d'application MQTT  avec STREAMLIT")
st.subheader("Affichage des données issues d'un accéleromètre MPU6050")   
mqtt_client.on_message = on_message

st.subheader("Exemple de graphique Plotly en temps réel")

#-------------création de 3 colonnes pour l'affichage des 3 graphiques -----------
col1, col2, col3 = st.columns(3)
with col1:
    st.write("gyroscope")
    graph1= st.empty()

with col2:
    st.write("accélérometre")
    graph2= st.empty()

with col3:
    st.write("température")
    graph3= st.empty()





#------------------------Boucle principale--------------------------
while True:        
    mqtt_client.loop()  # connexion au client mqtt
    
    #---------graphique 1 : donnees du gyroscope --------------
    fig1=go.Figure(data=[go.Scatter(y=gyro_x,mode='lines+markers', name="x")])
    fig1.add_trace(go.Scatter(y=gyro_y,mode='lines+markers',name="y"))
    fig1.add_trace(go.Scatter(y=gyro_z,mode='lines+markers',name="z"))
    
    #---------graphique 2 : donnees de l'accélérometre --------------
    fig2=go.Figure(data=[go.Scatter(y=accel_x,mode='lines+markers',name="x")]) 
    fig2.add_trace(go.Scatter(y=accel_y,mode='lines+markers',name="y"))
    fig2.add_trace(go.Scatter(y=accel_z,mode='lines+markers',name="z"))
    
    #---------graphique 3 : donnees du capteur de température --------------
    fig3=go.Figure(data=[go.Scatter(y=temp,mode='lines+markers')])   

    #---------------- graphique mis à jour en continu--------------------
    graph1.plotly_chart(fig1,use_container_width=True)
    graph2.plotly_chart(fig2,use_container_width=True)
    graph3.plotly_chart(fig3,use_container_width=True)
    
   


    

        

    
    
    