import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Aproxime o cartão para escrever...")
    
    # Escrever dados no cartão
    text = input("Digite o texto a ser gravado: ")
    reader.write(text)
    
    print("Dados gravados com sucesso!")

finally:
    GPIO.cleanup()