# sudo killall -TERM pigpiod
# sudo pigpiod
# python3 uart-soft-test.py 

import sys
import time
import difflib
import pigpio

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
                print(data.decode("utf-8").strip().replace('\x02', "\n"))
            time.sleep(.2)
    except UnicodeDecodeError:
        print("unicode error")
        print(data)
        print(len(data))
    except KeyboardInterrupt:
        print("good bye...")
    except Exception as e:
        print(e)
    finally:
        print("clean up") 
        pi.bb_serial_read_close(RX)
        pi.stop()
        sys.exit()
