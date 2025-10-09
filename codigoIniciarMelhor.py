#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import subprocess

# Configuração do LED
LED_VERDE = 17
LED_VERMELHO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_VERMELHO, GPIO.OUT)

# Configuração de tags e comandos específicos
TAGS_CONFIG = {
    "123456789": {
        "nome": "Tag Admin",
        "comando": "echo 'Administrador logado' && date"
    },
    "211547594069": {
        "nome": "Laica Tag", 
        "comando": "ffmpeg -f alsa -sample_rate 16000 -sample_fmt s16 -channels 1 -i hw:2,0 -acodec aac -b:a 64k -ar 16000 -ac 1 -f mpegts -listen 1 http://0.0.0.0:8080"  # Transmissão de áudio via HTTP
    },
    "555555555": {
        "nome": "Tag Sistema",
        "comando": "ls -la /home/pi/"
    }
}

reader = SimpleMFRC522()

def piscar_led(pin, vezes=3):
    """Pisca o LED indicado"""
    for _ in range(vezes):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.2)

def executar_comando(comando):
    """Executa um comando no terminal"""
    try:
        print(f"Executando: {comando}")
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✓ Comando executado com sucesso!")
            if resultado.stdout:
                print(f"Saída: {resultado.stdout}")
            return True
        else:
            print(f"✗ Erro: {resultado.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Erro ao executar: {e}")
        return False

print("Sistema de Controle de Acesso RFID")
print("Aproxime sua tag...")

try:
    while True:
        try:
            id, text = reader.read()
            tag_id = str(id)
            
            if tag_id in TAGS_CONFIG:
                config = TAGS_CONFIG[tag_id]
                print(f"✓ ACESSO PERMITIDO - {config['nome']}")
                piscar_led(LED_VERDE)
                
                # Executar comando específico da tag
                executar_comando(config['comando'])
                
            else:
                print("✗ ACESSO NEGADO - Tag não autorizada")
                piscar_led(LED_VERMELHO)
                
            time.sleep(2)
            
        except Exception as e:
            print(f"Erro na leitura: {e}")
            time.sleep(1)
            
except KeyboardInterrupt:
    print("\nSistema encerrado")
    
finally:
    GPIO.cleanup()