#!/usr/bin/env python

from tkinter import *
from tkinter import messagebox
import paho.mqtt.client as  mqtt
import paho.mqtt.subscribe as subscribe
from tkinter.ttk import *
import json
import threading
import time
import queue

q1=queue.Queue()
q2=queue.Queue()
q3=queue.Queue()
q4=queue.Queue()
go = threading.Event()


def on_connect(client, userdata, flags, rc):
    print("Connect")
    client.subscribe("prozentl")
    client.subscribe("prozentr")

def on_message(client, userdata, msg):
    print("recieved")
    if msg.topic == "prozentl":
        q1.put(msg.payload)
    if msg.topic == "prozentr":
        q2.put(msg.payload)

def publ():
    client.publish('steuerung', "links", qos=0, retain=False)
    print("Client publisht!")

def pubs():
    client.publish('steuerung', "stop", qos=0, retain=False)
    print("Client publisht!")

def pubr():
    client.publish('steuerung', "rechts", qos=0, retain=False)
    print("Client publisht!")

client=mqtt.Client()
client.connect("10.0.27.179",1883,60)
client.on_connect = on_connect
client.on_message = on_message
t2=threading.Thread(target=client.loop_forever,args=())

t2.start()

root = Tk()

frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
frame4 = Frame(root)

root.title("Wellenzahl")

label= Label(frame1,text="Wellenzahl - Füllstandsmessung",justify=LEFT)
label.pack(side=LEFT)

hi_there = Button(frame2,text="nach links",command=publ)
hi_there.pack(side=LEFT)

hi_there1 = Button(frame2,text="stop",command=pubs)
hi_there1.pack(side=RIGHT)

hi_there2 = Button(frame2,text="nach rechts",command=pubr)
hi_there2.pack()

#Warum wird "Vor Mainloop" nur einmal geprintet, trotz loop
bar1 = Progressbar(frame3, length=400)
bar1['value'] = q1.get()
bar1.pack()

bar2 = Progressbar(frame3, length=400)
bar2['value'] = q2.get()
bar2.pack()

def setze(q1,q3,q4):
    
    while True:
        if go.is_set():
            while(abs(float(100-var.get())-float(q1.get()))>5) and go.is_set():
                if float(100-var.get())>float(q1.get()):
                    print("publ von setzen")
                    pubr()
                else:
                    publ()
                    print("pubr von setzen")
            pubs()
        else:
            time.sleep(0.001)

t10=threading.Thread(target=setze, args=(q1,q3,q4))
t10.start()

def t10abrre():
    go.clear()

def t10mach():
    go.set()

var = DoubleVar()
scale1 = Scale(frame4, orient='vertical', from_ = 0, to = 100, variable = var) 
button401 = Button(frame4, text="Setze die Hoehe", command = t10mach)

button402 = Button(frame4, text="Abbrechen", command = t10abrre)
label401= Label(frame4,text=var.get())
scale1.pack()
button401.pack()
button402.pack()
label401.pack()

frame1.pack(padx=1,pady=1)
frame2.pack(padx=10,pady=10)
frame3.pack(padx=20,pady=20)
frame4.pack(padx=30, pady=30)

def hilf():
    while True:
        bar1['value'] = q1.get()
        bar2['value'] = q2.get()
        label401['text']= 100-var.get() 
        print("vor Mainloop")   

t1=threading.Thread(target=hilf,args=())
t1.start()

root.mainloop()
