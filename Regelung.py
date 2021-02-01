import paho.mqtt.client as  mqtt
import paho.mqtt.subscribe as subscribe
import json
import threading
import time
import queue

go = threading.Event()
q1=queue.Queue()
q2=queue.Queue()
q3=queue.Queue()


def on_connect(client, userdata, flags, rc):
    client.subscribe("prozentl")
    client.subscribe("prozentr")
    client.subscribe("regelung")

def on_message(client, userdata, msg):
    if msg.topic == "prozentl":
        q1.put(msg.payload)
    if msg.topic == "prozentr":
        q2.put(msg.payload)
    if msg.topic == "regelung":
            
        if (0 <= float(msg.payload) <= 100) :
            go.set()
            q3.put(msg.payload)
        else:
            go.clear()

client=mqtt.Client()
client.connect("10.0.27.179",1883,60)
client.on_connect = on_connect
client.on_message = on_message

def setze(q1,q2,q3):
    
    while True:
        if go.is_set():
            stell = float(q3.get())
            mess=abs(float(stell) - float(q2.get()))
                
            while mess >5:
                print(mess)
                if float(stell) > float(q1.get()):
                    print(stell)
                    print("publ von setzen")
                    client.publish('steuerung', "links", qos=0, retain=False)
                else:
                    client.publish('steuerung', "rechts", qos=0, retain=False)
                    print("pubr von setzen")
                mess=abs(float(100-stell) - float(q1.get()))
            client.publish('steuerung', "stop", qos=0, retain=False)
            go.clear()

        else:
            time.sleep(0.001)

t1=threading.Thread(target=setze, args=(q1,q2,q3))
t1.start()

t2=threading.Thread(target=client.loop_forever,args=())
t2.start()