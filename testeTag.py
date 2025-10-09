#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import os

class TesteRFIDCompleto:
    def __init__(self):
        # Configurar LED (opcional - GPIO 17)
        self.LED_PIN = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        
        self.leitor = SimpleMFRC522()
        self.tags_testadas = []
    
    def piscar_led(self, vezes=3):
        """Pisca o LED para feedback visual"""
        for i in range(vezes):
            GPIO.output(self.LED_PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.LED_PIN, GPIO.LOW)
            time.sleep(0.2)
    
    def beep(self):
        """Feedback sonoro (se speaker conectado)"""
        os.system('echo -e "\a"')  # Beep do sistema
    
    def testar_leitura(self):
        print("🎯 TESTE COMPLETO DE RFID")
        print("=" * 40)
        
        while True:
            print("\n📱 Aproxime a tag do leitor...")
            print("💡 Dica: Mova lentamente sobre o leitor")
            
            try:
                id, texto = self.leitor.read()
                
                # Feedback visual e sonoro
                self.piscar_led(2)
                self.beep()
                
                print("\n" + "✅" * 10)
                print("✅ TAG FUNCIONANDO!")
                print("✅" * 10)
                print(f"🆔 ID único: {id}")
                print(f"📝 Texto: {texto}")
                print(f"🔢 ID (hex): {hex(id)}")
                print(f"🔢 ID (str): {str(id)}")
                
                # Registrar tag testada
                if id not in self.tags_testadas:
                    self.tags_testadas.append(id)
                    print(f"📊 Total de tags diferentes: {len(self.tags_testadas)}")
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n\n🧹 Finalizando teste...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                time.sleep(0.5)
    
    def testar_gravacao(self):
        print("\n📝 TESTE DE GRAVAÇÃO")
        texto_teste = "TESTE_PYTHON_" + str(int(time.time()))
        
        print(f"Gravando: '{texto_teste}'")
        print("Aproxime a tag...")
        
        try:
            id = self.leitor.write(texto_teste)
            print(f"✅ Gravação bem-sucedida!")
            print(f"🆔 Tag ID: {id}")
            print(f"💾 Dados gravados: {texto_teste}")
            return True
        except Exception as e:
            print(f"❌ Erro na gravação: {e}")
            return False

if __name__ == "__main__":
    try:
        teste = TesteRFIDCompleto()
        
        # Teste de leitura
        teste.testar_leitura()
        
        # Perguntar se quer testar gravação
        input("\nPressione Enter para testar gravação...")
        teste.testar_gravacao()
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
    finally:
        GPIO.cleanup()
        print("\n🧼 GPIO limpo. Teste concluído!")