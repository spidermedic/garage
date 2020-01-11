#! usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep, time

# initialize GPIO pins
GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

# Uses the magnetic switches to determine if the door is open
GPIO.setup(22, GPIO.IN) # position_sensor A
GPIO.setup(23, GPIO.IN) # position_sensor B

# Relay to trigger the garage door switch
GPIO.setup(17, GPIO.OUT, initial = 1) # Door Relay A
GPIO.setup(27, GPIO.OUT, initial = 1) # Door Relay B


def operate_door(door):
    """ Opens and closes the garage doors """

    # Assign GPIO pins based on which door was requested
    if door == 'A':
        door_relay = 17
        position_sensor = 22
    if door == 'B':
        door_relay = 27
        position_sensor = 23

    # If the door is closed, momentarily trigger the switch to open it
    if GPIO.input(position_sensor) == 0:
        GPIO.output(door_relay, 0)
        sleep(0.25)
        GPIO.output(door_relay, 1)
        sleep(15)

    # If the door is open, keep the switch on until it the position_sensor
    # reads as closed or for a max of 15 seconds.
    else:
        GPIO.output(door_relay, 0)
        start = time()
        while GPIO.input(position_sensor) == 1 and time()-start < 15:
            pass

        GPIO.output(door_relay, 1)
        sleep(0.25)


def get_door_status():
    """ Returns the current open/closed state for each door """

    #Set default reading as closed
    door_a = 'closed'
    door_b = 'closed'

    # Check to see if either door is open
    if GPIO.input(22):
        door_a = 'open'
    if GPIO.input(23):
        door_b = 'open'

    return (door_a, door_b)