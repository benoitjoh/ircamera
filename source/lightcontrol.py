#!/usr/local/bin/python3

import RPi.GPIO as GPIO
import time
import os

#Limit of the measurement that indicates the line between dark and bright
LIMIT = 37000 
HYSTERESIS =  2000

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
    """
    this method reads "analog" input from a digital pin
    the pin is set to low, and then it slowly returns high depending from 
    status of the resistor
    the recovery time is returned in microseconds
    """

    #set pin to Output and set it to LOW 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    time.sleep(0.1)

    start_ns = time.time_ns()
    GPIO.output(pin_to_circuit, GPIO.LOW)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
    
    #Count until the pin returns to high again
    while (GPIO.input(pin_to_circuit) == GPIO.LOW ):
        time.sleep(0.0001)
     
    end_ns = time.time_ns()
    delta_ns = end_ns - start_ns
    delta_mys = delta_ns // 1000
    return delta_mys

state = 'BRIGHT'

# --- main loop ---------------------------
# loop and check every second light. 
# if dark enough turn on light.


state = 'BRIGHT'

try:
    # Main loop
    while True:

        delta_mys = rc_time(pin_ldr)
 
        if delta_mys >= LIMIT:
            state = 'DARK'
        elif delta_mys < LIMIT - HYSTERESIS:
            state = 'BRIGHT'

        print ("%imic  --> %s " % (delta_mys, state))

        if 1:
            if state == 'DARK':
                GPIO.output(pin_out_small, GPIO.HIGH)
                GPIO.output(pin_out_big, GPIO.HIGH)
            else:
                GPIO.output(pin_out_small, GPIO.LOW)
                GPIO.output(pin_out_big, GPIO.LOW)

        time.sleep(1)


except KeyboardInterrupt:
    pass

finally:
    GPIO.output(pin_out_small, GPIO.LOW)
    GPIO.output(pin_out_big, GPIO.LOW)
    GPIO.cleanup()
