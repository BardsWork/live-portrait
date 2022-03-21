#!/usr/bin/env python3

# LIBRARIES
import sys
import time
from src import sensor
from src import player
from pathlib import Path

# VARIABLES
VIDEO_PATH = Path("/home/pi/VIDEO.mp4")  # Path to video
DISTANCE = 10  # Distance at which to trigger the video (in cm)


def main():
    try:
        omx_player = player.initialize(VIDEO_PATH)

        while True:
            omx_player.pause()
            try:
                calculated_distance = sensor.calculate_distance()
                if calculated_distance <= DISTANCE:
                    omx_player.play()
                    time.sleep(omx_player.duration())
                else:
                    pass

                omx_player.set_position(0.0)
            except ValueError:
                print("--- ERROR: Sensor was not initialized. ---")
                end_program()

    except KeyboardInterrupt:
        end_program()


def end_program():
    """Close application with keyboard input.

    To exit, hit Control + X. You may have to hit it twice.
    """

    print("STATUS: Closing Program")

    player.close()
    sensor.cleanup()
    sys.exit()


main()
