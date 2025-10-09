#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def verificar_tag_rapido():
    leitor = SimpleMFRC522()
    
    print("🔍 Verificando tag...")
    
    try:
        id, texto = leitor.read()
        
        print(f"🆔 ID: {id}")
        
        # Verificações simples
        if texto.strip() == "":
            print("❌ TAG VAZIA - Não contém dados")
        elif len(texto.strip()) < 3:
            print("⚠️  TAG COM POUCOS DADOS - Possivelmente não utilizada")
        else:
            print(f"✅ TAG GRAVADA - Contém: {texto.strip()}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        GPIO.cleanup()

# Executar verificação
verificar_tag_rapido()