# ADC
from machine import Pin
from machine import ADC
adc = ADC(0)
ir = Pin(2,Pin.OUT)
ir.value(0) # Enable IR diode so that we can receive what is reflected back
print(f"Distance Sensor: {adc.read()}")


# Neopixel does not currently work
import neopixel
from machine import Pin
np = neopixel.NeoPixel(Pin(16),1)
np.fill((100,100,100))
np.write()


# Read temperature and Humidity
from machine import Pin, SoftI2C
from hdc1080 import HDC1080

scl = Pin(5, Pin.IN, Pin.PULL_UP)
sda = Pin(4, Pin.IN, Pin.PULL_UP)
i2c = SoftI2C(scl,sda)
temp = HDC1080(i2c)
print(f"Temperature {temp.temperature()}°C")
print(f"Humidity {temp.humidity()}%")


# Nod hello
import machine
import time

from uln2003 import Stepper, HALF_STEP, FULL_STEP, FULL_ROTATION
from machine import Pin

stepper = Stepper(HALF_STEP, Pin(13, Pin.OUT), Pin(12, Pin.OUT), Pin(14, Pin.OUT), Pin(15, Pin.OUT), delay=.003 )  
mode = Pin(0, Pin.IN)


clockwise = -1

dir = -clockwise
# Rotate a half rotation into the correct direction
if adc.read() < 700:
    dir = clockwise

stepper.step(FULL_ROTATION*0.3, dir)
start_time = time.time()
BUTTON_ACTIVE = 0
while time.time() - start_time < 8:
    # Rotate in steps
    # Change direction when button is pressed
    stepper.step(FULL_ROTATION/10, dir)
    #     time.sleep(1)
    if mode() == BUTTON_ACTIVE:
        print("Mode pressed: Change direction")
        dir = dir * -1
        time.sleep(0.4) # debounce
        
while True:
    
    hour = time.gmtime()[3]
    minute = time.gmtime()[4]
    print(f"It's {hour}:{minute:02d}")
    if hour == 7 and minute == 33:
        # Ring the bell at the specific time
        stepper.step(FULL_ROTATION, dir)
    time.sleep(30)