# Nod hello
import machine
import time

from uln2003 import Stepper, HALF_STEP, FULL_STEP, FULL_ROTATION
from machine import Pin

stepper = Stepper(HALF_STEP, Pin(13, Pin.OUT), Pin(12, Pin.OUT), Pin(14, Pin.OUT), Pin(15, Pin.OUT), delay=.003 )  
mode = Pin(0, Pin.IN)
MODE_ACTIVE=0

clockwise = -1

## MQTT
import secrets
import time
import ubinascii
from umqttsimple import MQTTClient

client = None
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = secrets.mqtt.topic
topic_pub = secrets.mqtt.topic
mqtt_server = secrets.mqtt.host
mqtt_port = secrets.mqtt.port
mqtt_user = secrets.mqtt.user
mqtt_password = secrets.mqtt.password

# TODO: Reduce the Keep alive time once #5 is implemented
KEEPALIVE = 3 * 60 * 60 # 3 hours

timer_active = False
timer_delay = 0

def sub_cb(topic, msg):
    global timer_active, timer_delay
    # print((topic, msg))
    if topic == b'timer':
        import json
        timer_data = None
        try:
            timer_data = json.loads(msg)
            seconds = int(timer_data['seconds'])
            title = timer_data['title']
            print(f"Start the timer '{title}' with {seconds} seconds")

            timer_active = True
            timer_delay = seconds
        except KeyError as e:
            print("Ignoring badly formatted or unknown JSON")
            print(msg)
            pass
        except ValueError as e:
            pass


def connect_and_subscribe():
    global client, client_id, mqtt_server, topic_sub, mqtt_port, mqtt_user, mqtt_password,sub_cb
    try:
      print("connecting to MQTT...")
      client = MQTTClient(client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password, keepalive=KEEPALIVE)
      client.set_last_will(topic_pub, '{ "status":"offline"} ', retain=False, qos=0)
      client.set_callback(sub_cb)
      client.connect()
      print(f"Connection succeeded: {client.connect() == 0}")
      client.subscribe(topic_sub)
      client.publish(topic_pub, bytes('{"status":"hello"}', 'utf-8'))
      print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    except OSError as e:
        restart_and_reconnect(e)


def restart_and_reconnect(error):
  print(f"Failed to connect to MQTT broker. Due to error {error} Reconnecting...")
  # TODO attempt to reconnect instead
  machine.reset()

connect_and_subscribe()

last_ping = time.time()
delay = .5
while True:
    try:
        client.check_msg()
    except OSError as e:
        print(f"Erron in main loop: {e} Reconnecting")
        client.set_callback = None
        client = None
        print("gc.collect()")
        import gc
        gc.collect()
        connect_and_subscribe()
    
    if mode() == MODE_ACTIVE:
        stepper.step(FULL_ROTATION, clockwise)
    
    if time.time() - last_ping > (KEEPALIVE):
        print("ping")
        client.ping()
        last_ping = time.time()
    
    if timer_active:
        timer_active = False
        time.sleep(timer_delay)
        print("Ringing the bell")
        stepper.step(FULL_ROTATION, clockwise)    

    time.sleep(delay)
