import streamlit as st
import mysql.connector
import paho.mqtt.client as mqtt
#import sqlite3
import time
import pandas as pd


#------------configuration du broker et des topics ------------------------
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883

#---------liste des topics -----------------------------------

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
#----3 pour le gyroscope----3 pour l'accélérometre#----1 pour la température
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
#--------------fonction permettant d'envoyer un message au broker mqtt ------------------
def send_message(rap_cyc,topic):
    message = str(rap_cyc)
    mqtt_client.publish(topic,message)

# fonction permettant de recevoir les messages envoyer par le broker mqtt et de les stocker
def on_message(client,userdata,message):
#----------gyroscope axe x------------
    if message.topic == mqtt_topic1 :
        new_data = message.payload.decode("utf-8")
        gyro_x.append(float(new_data))
#----------gyroscope axe y------------    
    if message.topic == mqtt_topic2 :
        new_data = message.payload.decode("utf-8")
        gyro_y.append(float(new_data))
#----------gyroscope axe z------------    
    if message.topic == mqtt_topic3 :
        new_data = message.payload.decode("utf-8")
        gyro_z.append(float(new_data))
#----------accélérometre axe x------------        
    if message.topic == mqtt_topic4 :
        new_data = message.payload.decode("utf-8")
        accel_x.append(float(new_data))
#----------accélérometre axe y------------             
    if message.topic == mqtt_topic5 :
        new_data = message.payload.decode("utf-8")
        accel_y.append(float(new_data))
#----------accélérometre axe z------------           
    if message.topic == mqtt_topic6 :
        new_data = message.payload.decode("utf-8")
        accel_z.append(float(new_data))
#----------température---------------------      
    if message.topic == mqtt_topic7 :
        new_data = message.payload.decode("utf-8")
        temp.append(float(new_data))   

#----------Fonction permettant la connexion à la base de données MySql-------
#def create_connection():
#    connection = mysql.connector.connect(
#        host='localhost',
#        user='root',
#        password='sdf',
#        database='donnee_seisme'
#   )
#    return connection

mqtt_client.on_message = on_message  
st.title("Enregistrement des données sismiques d'un tremblement de terre")
nom = st.text_input('Veuillez nommer votre essai')
st.write('nom de votre essai :  ', nom)

#--------------commande du moteur latérale------------------
puissance_lat = st.slider("Puissance lattérale du seisme en %",min_value=0.0,max_value=12.0,value=0.0,step=0.1)
rc_lat=int(330+(puissance_lat*693/12))

#--------------commande du moteur longitudinale------------------
puissance_long = st.slider("Puissance longitudinuale du seisme en %",min_value=0.0,max_value=12.0,value=0.0,step=0.1)
rc_long=int(330+(puissance_long*693//12))

duree_enr = st.number_input("Durée de l'enregistrement en secondes",min_value=1,max_value=10,value=1,step=1)
enr=st.button("enregistrer")
text = "enregistrement en cours. Please wait."
my_bar = st.progress(0, text=text)   
if enr:
    duree=0
    now=time.time()
    send_message(rc_lat,"test/pwm_lat")
    send_message(rc_long,"test/pwm_long")  
    while duree<duree_enr :        
        my_bar.progress(int(duree/duree_enr*100), text=text)
        mqtt_client.loop()       
        duree=(time.time()-now)
    
send_message(0,"test/pwm_lat")
send_message(0,"test/pwm_long")
mqtt_client.disconnect()
df = pd.DataFrame(list(zip(gyro_x,gyro_y,gyro_z,accel_x,accel_y,accel_z,temp)), columns = ['gyro_x','gyro_y',"gyro_z","accel_x","accel_y","accel_z","temp"])
st.write(df)
st.write("enregistrement terminé")
