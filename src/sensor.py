"""Sensor


Args:
    PIN_TRIGGER: corresponds to the actual pin on the raspberry pi.
      This is how the program knows what to listen to.
    PIN_ECHO: corresponds to the actual pin on the raspberry pi.
      This is how the program knows where to send the signal.
"""

import time
import RPi.GPIO as GPIO

_INITIALIZED = False  # track if the sensor was initialized.

# Set pins that are connected to RPI
_PIN_TRIGGER = 7
_PIN_ECHO = 11


def initialize():
    """Initializes the sensor for more consistent reading on startup.

    Returns:
        sensor status.
    """

    global _INITIALIZED

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(_PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(_PIN_ECHO, GPIO.IN)

    if not _INITIALIZED:
        GPIO.output(_PIN_TRIGGER, GPIO.LOW)
        time.sleep(2)
        _INITIALIZED = True

    return _INITIALIZED


def calculate_distance():
    """Calculates the distance via Sonar sensor.

    Raises:
        ValueError - sensor was not initialized
    Returns:
         detected distance in centimeters
    """
    pulse_start_time = 0
    pulse_end_time = 0

    sensor_status = initialize()

    if not sensor_status:
        raise ValueError('ERROR - Sensor is not initialized!!!')

    GPIO.output(_PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)  # Have to wait to receive signal.
    GPIO.output(_PIN_TRIGGER, GPIO.LOW)

    # Determine if current signal is start or end time.
    while GPIO.input(_PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(_PIN_ECHO) == 1:
        pulse_end_time = time.time()

    # Formula: duration * sonic speed (34300 cm/s) divided by 2 (round trip).
    return round((pulse_end_time - pulse_start_time) * 34300 / 2, 2)


def cleanup():
    """Releases the GPIO pins.
    If this is not performed, Python will throw a warning the next time
    you run the program.
    """

    GPIO.cleanup()
