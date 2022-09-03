#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os, signal
import time

GPIO_BTN_PIN = 26
GPIO_BTN_SRC = 20
LED_PIN = 21

def on():
    GPIO.output(LED_PIN, GPIO.HIGH)

def off():
    GPIO.output(LED_PIN, GPIO.LOW)

def btn_pressed(arg0):
    print(f"button pressed: {arg0} {GPIO.input(GPIO_BTN_PIN)}")
    process_btn_hold()

def process_btn_hold():
    if GPIO.input(GPIO_BTN_PIN) == GPIO.LOW:
        print("process button hold - but GPIO is low")
        return

    print("process button hold")
    total_time = 3
    check_interval = 0.01
    start_time = time.time()
    hold_time = 0

    while GPIO.input(GPIO_BTN_PIN) == GPIO.HIGH and hold_time < total_time:
        print(GPIO.input(GPIO_BTN_PIN), hold_time)
        if hold_time > 0.1:
            on()
        if GPIO.input(GPIO_BTN_PIN) == GPIO.LOW and hold_time > 0.5:
            break
        hold_time = time.time() - start_time
        time.sleep(check_interval)

    if hold_time > total_time:
        print("timeout reached")
        off()
    else:
        print("button released early")
        off()


def init():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GPIO_BTN_SRC, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(GPIO_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_BTN_PIN, GPIO.RISING, callback=btn_pressed, bouncetime=500)

    on()
    time.sleep(2)
    off()

if __name__ == "__main__":
    init()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            GPIO.cleanup()
            os.kill(os.getpid(), signal.SIGTERM)
