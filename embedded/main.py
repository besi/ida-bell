# Nod hello
import machine
import time

from uln2003 import Stepper, HALF_STEP, FULL_STEP, FULL_ROTATION
from machine import Pin

stepper = Stepper(HALF_STEP, Pin(13, Pin.OUT), Pin(12, Pin.OUT), Pin(14, Pin.OUT), Pin(15, Pin.OUT), delay=.003 )  
mode = Pin(0, Pin.IN)


clockwise = -1
dir = clockwise

start_time = time.time()
BUTTON_ACTIVE = 0
i = 0
print("Grant 3 seconds to change the direction by pressing mode")
while time.time() - start_time < 3:
    # Rotate in steps
    # Change direction when button is pressed
    stepper.step(FULL_ROTATION/10, dir)
    i = i + (FULL_ROTATION/10 * dir)
    if mode() == BUTTON_ACTIVE:
        print("Mode pressed: Change direction")
        dir = dir * -1
        time.sleep(0.4) # debounce
print("Remaining steps")
print(i)
stepper.step(FULL_ROTATION - abs(i), dir)
time.sleep(1)
## MQTT
import secrets
import time
import ubinascii
from umqttsimple import MQTTClient

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = secrets.mqtt.topic
topic_pub = secrets.mqtt.topic
mqtt_server = secrets.mqtt.host
mqtt_port = secrets.mqtt.port
mqtt_user = secrets.mqtt.user
mqtt_password = secrets.mqtt.password

 

def sub_cb(topic, msg):
    # print((topic, msg))
    if topic == b'timer':
        import json
        timer_data = json.loads(msg)
        seconds = int(timer_data['seconds'])
        title = timer_data['title']
        print(f"Start the timer '{title}' with {seconds} seconds")

        time.sleep(seconds)
        print("Ringing the bell")
        stepper.step(FULL_ROTATION, dir)
        

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub, mqtt_port, mqtt_user, mqtt_password,sub_cb
  client = MQTTClient(client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password,keepalive=60)
  client.set_callback(sub_cb)
  print(f"Connecting... {client.connect() == 0}")
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  # TODO attempt to reconnect instead
  machine.reset()

try:
  print("connecting to MQTT")
  client = connect_and_subscribe()
  while True:
    client.check_msg()
    time.sleep(0.25)
    client.ping()
except OSError as e:
    import errno
    error = errno.errorcode[e.errno]
    print(f"Error {error}")
    restart_and_reconnect()
        
while True:
    
    hour = time.gmtime()[3]
    minute = time.gmtime()[4]
    print(f"It's {hour}:{minute:02d}")
    if hour == 7 and minute == 33:
        # Ring the bell at the specific time
        stepper.step(FULL_ROTATION, dir)
    time.sleep(30)