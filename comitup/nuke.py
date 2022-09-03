import logging
import os
import signal
import time
from functools import wraps

enabled = False
try:
    import RPi.GPIO as GPIO

    enabled = True
except ModuleNotFoundError:
    pass

from comitup import status_led  # noqa
from comitup import config  # noqa
from comitup import nm  # noqa

GPIO_BTN_PIN = 26
GPIO_BTN_SRC = 20

log = logging.getLogger("comitup")

def checkenabled(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not enabled:
            return

        (conf, _) = config.load_data()
        if not conf.getboolean("enable_nuke"):
            return

        return fn(*args, **kwargs)

    return wrapper


@checkenabled
def nuke():
    for ssid in nm.get_all_wifi_connection_ssids():
        nm.del_connection_by_ssid(ssid)

    log.warning("configuration nuked, rebooting")
    os.system("shutdown -r now 'comitup config nuked'")
    # os.kill(os.getpid(), signal.SIGTERM)


def gpio_callback(dummy):
    log.debug("Nuke start event detected")
    status_led.on()
    process_button_event()


def process_button_event():
    if GPIO.input(GPIO_BTN_PIN) == GPIO.LOW:
        return

    total_time = 3
    check_interval = 0.01
    start_time = time.time()
    hold_time = 0

    while GPIO.input(GPIO_BTN_PIN) and hold_time < total_time:
        if hold_time > 0.5:
            status_led.on()
        if GPIO.input(GPIO_BTN_PIN) == GPIO.LOW and hold_time > 0.5:
            break
        hold_time = time.time() - start_time
        time.sleep(check_interval)

    if hold_time > total_time:
        log.warning("Nuke function invoked")
        status_led.blink(5)
        nuke()
    else:
        log.info("nuclear war averted")
        status_led.off()

@checkenabled
def init_nuke():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(GPIO_BTN_SRC, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(GPIO_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_BTN_PIN, GPIO.RISING, callback=gpio_callback, bouncetime=200)

    # So maybe the pin is already shorted?
    process_button_event()


@checkenabled
def cleanup_nuke():
    GPIO.remove_event_detect(GPIO_BTN_PIN)
    GPIO.setup(GPIO_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
