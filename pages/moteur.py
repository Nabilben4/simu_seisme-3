import streamlit as st
import paho.mqtt.client as mqtt
import time
#-------configuration du broker------------
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic = "test/pwm"

#-------config client-----
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker, mqtt_port)

 #------fonction envoi de massage-----------------   
def send_message(rap_cyc):
    message = str(rap_cyc)
    mqtt_client.publish(mqtt_topic, message)

st.title("Exemple d'application MQTT  avec STREAMLIT")
st.subheader("Commande d'un moteur à courant continu par PWM")
puissance = st.slider("Puissance du seisme en %",min_value=1,max_value=100,value=1,step=1)
rc=int(puissance*1023//100)
send_message(rc)
mqtt_client.loop()
    
    
   
    
   