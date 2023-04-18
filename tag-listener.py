import subprocess

import paho.mqtt.client as mqtt

host = 'stereopida.local'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT server '%s'" % host)
    client.subscribe("services/rfid/#")


def on_message(client, userdata, msg):
    handleMessage(msg)

def execute_shell(commands):
    subprocess.call(commands)


def handleMessage(msg):
    tag = msg.payload.decode("utf-8").strip()
    print(tag)
    execute_shell(['aplay', 'bell.wav'])


client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31, transport="tcp")
client.on_connect = on_connect
client.on_message = on_message
client.connect(host)
client.loop_forever()
