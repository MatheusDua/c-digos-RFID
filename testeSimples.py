#!/usr/bin/env python3

import RPi.GPIO as GPIO
import spidev
import time

# Testar comunicação SPI
try:
    spi = spidev.SpiDev()
    spi.open(0, 0)  # bus 0, device 0
    spi.max_speed_hz = 1000000
    print("SPI comunicando corretamente!")
    spi.close()
except Exception as e:
    print(f"Erro SPI: {e}")

# Testar GPIO
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(25, GPIO.HIGH)
    print("GPIO funcionando!")
    GPIO.cleanup()
except Exception as e:
    print(f"Erro GPIO: {e}")