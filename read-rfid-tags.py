# sudo killall -TERM pigpiod; sudo pigpiod
# python3 read-rfid-tags.py

import sys
import time
import difflib
import pigpio
import paho.mqtt.publish as publish
import time

mqtt_host = 'localhost'
lastTag = None
lastTime = 0

RX=24

while True:
    try:
        pi = pigpio.pi()
        pi.set_mode(RX, pigpio.INPUT)
        pi.bb_serial_read_open(RX, 9600, 8)
    
        print("DATA - SOFTWARE SERIAL:")
        while 1:
            (count, data) = pi.bb_serial_read(RX)
            if count > 3:
                tags = []
                try:
                    tags = data.decode("utf-8").strip().replace('\x02', "\n").replace('\x03','').split("\n")
                except UnicodeDecodeError:
                    print("unicode error")
                for tag in tags:
                    if len(tag) == 12:
                        tag = tag[0:-2]
                        freshTag = (not tag == lastTag)
                        if freshTag or (time.time() - lastTime) > 1:
                            lastTag = tag
                            lastTime = time.time()
                            print(tag)
                            publish.single('services/rfid/tagged/', tag, hostname=mqtt_host)
            time.sleep(.1)
    except KeyboardInterrupt:
        print("\nQuitting...")
    except Exception as e:
        print(e)
    finally:
        print("Cleaning up...") 
        pi.bb_serial_read_close(RX)
        pi.stop()
        sys.exit()
