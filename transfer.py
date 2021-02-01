#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import time

class mqtttransfer:
    def __init__(self, ip, port, height = 0.2):
        self.client=mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(ip, port, 60)
        self.client.loop_start()
        self._hoehe=height

    def on_connect(self, client, userdata, flags, rc): 
        client.subscribe("radar/radar:tier1")

    def on_message(self, client, userdata, msg):
        x=json.loads(msg.payload)
        targets = x["targets"]
        wert1 = ((0.36-targets[0])/self._hoehe)*100
        #print("wert1:", wert1)
        print(repr(wert1))
        self.client.publish("prozentl", wert1)
        self.client.publish("prozentr", wert1)

if __name__=="__main__":
    mqtt=mqtttransfer("10.0.27.179", 1883)

    try:
        while(True):
            time.sleep(10)
    except KeyboardInterrupt:
        print("finish")
