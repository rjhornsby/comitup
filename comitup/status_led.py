"""
status_led.py

Add support to blink the green led on a Raspberry pi one time, for a half sec.

https://mlagerberg.gitbooks.io/raspberry-pi/content/5.2-leds.html
"""
import sys

import RPi.GPIO as GPIO
import time
import getpass

sys.stderr.write(f"EUSER is {getpass.getuser()}\n")
sys.stderr.flush()

if not GPIO.getmode():
    GPIO.setmode(GPIO.BCM)

LED_PIN = 20
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)


def can_blink() -> bool:
    return True


def on() -> None:
    """Turn on the LED"""
    GPIO.output(LED_PIN, GPIO.HIGH)


def off() -> None:
    """Turn off the LED"""
    GPIO.output(LED_PIN, GPIO.LOW)


def blink(times: int = 1) -> None:
    """Blink the green led n times."""

    for _ in range(times):
        on()
        time.sleep(0.25)
        off()
        time.sleep(0.25)


if __name__ == "__main__":
    blink(3)
