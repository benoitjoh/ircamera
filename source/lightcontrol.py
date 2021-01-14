#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
import os

MOTIONSTATEFILE = '/tmp/motionevent'
LIMIT = 2350 
HYSTERESIS =  200

GPIO.setmode(GPIO.BOARD)

#define the pins
pin_ldr = 7       # input for light detecting resistor 
pin_out_small = 3 # output for small light unit 
pin_out_big = 5   # output for big light


GPIO.setup(pin_out_small, GPIO.OUT)
GPIO.setup(pin_out_big, GPIO.OUT)

# blink led for init sign.. 
x = 0
while x<5:
    GPIO.output(pin_out_small, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(pin_out_small, GPIO.HIGH)
    time.sleep(0.2)
    x += 1

def rc_time (pin_to_circuit):
    # this reads "analog" input from a digital pin
    count = 0

    #set pin to Output and set it to LOW 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
    
    #Count until the pin returns to high again
    while (GPIO.input(pin_to_circuit) == GPIO.LOW and count < LIMIT +  100):
        count += 1
    #    time.sleep(0.01)
    return count

state = 'BRIGHT'

# --- main loop ---------------------------
# loop and check every second light. 
# if dark enough turn on light.


state = 'BRIGHT'

try:
    # Main loop
    while True:

        value = rc_time(pin_ldr)
        print value, state
 
        if value >= LIMIT:
            state = 'DARK'
        elif value < LIMIT - HYSTERESIS:
            state = 'BRIGHT'


        if 1:
            if state == 'DARK':
                GPIO.output(pin_out_small, GPIO.HIGH)
                GPIO.output(pin_out_big, GPIO.HIGH)
            else:
                GPIO.output(pin_out_small, GPIO.LOW)
                GPIO.output(pin_out_big, GPIO.LOW)

        time.sleep(2)


except KeyboardInterrupt:
    pass

finally:
    GPIO.output(pin_out_small, GPIO.LOW)
    GPIO.output(pin_out_big, GPIO.LOW)
    GPIO.cleanup()
