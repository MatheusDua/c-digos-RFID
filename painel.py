from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import RPi.GPIO as GPIO

# Configurações da janela
Window.size = (800, 480)  # Tamanho da tela de 7"
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Cor de fundo

# Configuração do GPIO
GPIO.setmode(GPIO.BCM)
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

class Painel(BoxLayout):
    led_ligado = False

    def alternar_led(self):
        """Alterna o estado do LED"""
        self.led_ligado = not self.led_ligado
        GPIO.output(LED_PIN, self.led_ligado)
        self.ids.estado.text = "LED Ligado" if self.led_ligado else "LED Desligado"
        self.ids.estado.color = (0, 1, 0, 1) if self.led_ligado else (1, 0, 0, 1)

class PainelApp(App):
    def build(self):
        return Painel()

    def on_stop(self):
        """Limpa GPIO ao fechar o app"""
        GPIO.cleanup()

if __name__ == "__main__":
    PainelApp().run()
