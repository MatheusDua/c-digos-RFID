#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

def testar_com_celular():
    leitor = SimpleMFRC522()
    
    print("📱 TESTE COM CELULAR NFC")
    print("=" * 40)
    print("1. Instale 'NFC Tools' no celular")
    print("2. Vá em 'Outras' > 'Emular tag'")
    print("3. Aproxime o celular do leitor RFID")
    print("4. O celular vibrará quando detectado")
    print("=" * 40)
    
    try:
        while True:
            print("\n⏳ Aguardando celular/tag...")
            id, texto = leitor.read()
            
            print(f"✅ DISPOSITIVO DETECTADO!")
            print(f"🆔 ID: {id}")
            print(f"📝 Conteúdo: {texto}")
            print(f"🔢 Tipo: {'Celular NFC' if id > 1000000 else 'Tag RFID comum'}")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nTeste finalizado!")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        GPIO.cleanup()

testar_com_celular()