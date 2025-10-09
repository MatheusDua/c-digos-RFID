#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import subprocess  # Adicionado para executar comandos no terminal

# Configuração do LED (opcional)
LED_VERDE = 17
LED_VERMELHO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_VERMELHO, GPIO.OUT)

# Tags autorizadas (substitua pelos IDs das suas tags)
TAGS_AUTORIZADAS = {
    "123456789",  # Exemplo de ID
    "987654321"   # Exemplo de ID
}

# Comando a ser executado quando acesso for permitido
# Exemplos de comandos (descomente o que desejar ou adicione seus próprios):
COMANDO_PERMITIDO = "ffmpeg -f alsa -sample_rate 16000 -sample_fmt s16 -channels 1 -i hw:2,0 -acodec aac -b:a 64k -ar 16000 -ac 1 -f mpegts -listen 1 http://0.0.0.0:8080"  # Transmissão de áudio via HTTP
# COMANDO_PERMITIDO = "ls -la"  # Listar arquivos
# COMANDO_PERMITIDO = "date"    # Mostrar data e hora
# COMANDO_PERMITIDO = "python3 /caminho/para/seu/script.py"  # Executar outro script

reader = SimpleMFRC522()

def piscar_led(pin, vezes=3):
    """Pisca o LED indicado"""
    for _ in range(vezes):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.2)

def executar_comando(comando):
    """Executa um comando no terminal e retorna o resultado"""
    try:
        print(f"Executando comando: {comando}")
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✓ Comando executado com sucesso!")
            if resultado.stdout:
                print(f"Saída: {resultado.stdout}")
        else:
            print(f"✗ Erro ao executar comando: {resultado.stderr}")
            
        return resultado.returncode == 0
        
    except Exception as e:
        print(f"✗ Erro ao executar comando: {e}")
        return False

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
                
                # Executar comando quando acesso for permitido
                executar_comando(COMANDO_PERMITIDO)
                
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