#!/usr/bin/env python3

# LIBRARIES
import sys
import RPi.GPIO as GPIO
import time
from omxplayer.player import OMXPlayer
from pathlib import Path

# Set constant values.
# Any variables in all caps should not be changed whent he program is running.

# Set pins that are connected to RPI 
PIN_TRIGGER = 7
PIN_ECHO = 11

# Default video path
VIDEO_PATH = Path("/home/pi/grandpa.mp4")

# Distance at which to trigger the video (in cm)
DISTANCE_SENSITIVITY = 10

# GPIO SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

# DEBUG values
play_count = 0

# Calculate distance via Sonar sensor
def distance():
    # Setting the trigger to low allows the sensor to settle
    # per tutorial, this should provide more consistent results.
    # GPIO.output(PIN_TRIGGER, GPIO.LOW)
    # time.sleep(2)
    #
    # I commented this section out as I'm not sure how useful this is in Live Portrait application
    
    print("Calculating distance...")
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    
    # Timer to allow the sensor to receive a reading
    time.sleep(0.00001)
    
    # Turn off sensor to process reading
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    
    # Process returned data
    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()

    # OUTPUT
    pulse_duration = pulse_end_time - pulse_start_time
    # durantion * sonic speed (34300 cm/s)
    # divide by 2 since we're doing a round trip (there/back)
    distance = round(pulse_duration * 34300 / 2, 2)
    print("Distance = %.1f cm" % distance)
    
    return distance

try:
    player = OMXPlayer(VIDEO_PATH, args=['--no-osd', '--loop'])
    # sleep is here for the player to have enough time to load the video into the buffer.
    # different videos may require different buffer time.
    # NOTE: I noticed that a longer sleep timer causes the video to start playing before pausingm adjust as necessary.
    time.sleep(0.55)
    print("Ready to trigger")
    
    # Program loop
    while True:
        player.pause()
        calculated_distance = distance()
        
        if( calculated_distance <= DISTANCE_SENSITIVITY):
            print("Trigger count {}".format(play_count))
            player.play()
            time.sleep(player.duration())
            play_count += 1
        else:
            pass
        
        player.set_position(0.0)
        
except KeyboardInterrupt:
    player.quit()
    GPIO.cleanup()
    sys.exit()
        
