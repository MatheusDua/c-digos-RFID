from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

class CameraApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)  # /dev/video0
        layout = BoxLayout(orientation='vertical')
        self.img = Image()
        layout.add_widget(self.img)

        btn = Button(text='Capturar Foto', size_hint=(1, 0.2))
        btn.bind(on_press=self.capturar_foto)
        layout.add_widget(btn)

        Clock.schedule_interval(self.atualizar, 1.0 / 30.0)  # 30 FPS
        return layout

    def atualizar(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tobytes()
            textura = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            textura.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = textura

    def capturar_foto(self, instance):
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite('foto.jpg', frame)
            print("📸 Foto salva como foto.jpg")

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    CameraApp().run()
