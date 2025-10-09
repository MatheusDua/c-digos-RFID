#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

# Configuração do LED (opcional)
LED_VERDE = 17
LED_VERMELHO = 27

GPIO.setmode(GPIO.BCM)

# Tags autorizadas (substitua pelos IDs das suas tags)
TAGS_AUTORIZADAS = {
    "123456789",  # Exemplo de ID
    "987654321"   # Exemplo de ID
}

reader = SimpleMFRC522()

def piscar_led(pin, vezes=3):
    """Pisca o LED indicado"""
    for _ in range(vezes):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.2)

print("Sistema de Controle de Acesso RFID")
print("Aproxime sua tag...")

try:
    while True:
        try:
            id, text = reader.read()
            tag_id = str(id)
            
            if tag_id in TAGS_AUTORIZADAS:
                print("✓ ACESSO PERMITIDO")
                piscar_led(LED_VERDE)
            else:
                print("✗ ACESSO NEGADO")
                piscar_led(LED_VERMELHO)
                
            time.sleep(2)
            
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(1)
            
except KeyboardInterrupt:
    print("\nSistema encerrado")
    
finally:
    GPIO.cleanup()