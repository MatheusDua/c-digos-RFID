import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import subprocess
import shlex
import os

# Define uma cor de fundo (opcional)
Window.clearcolor = (0.15, 0.15, 0.15, 1)

class LoginScreen(Screen):
    """Screen que contém o formulário de login. A estrutura visual
    é definida em 'painel.kv'.
    """

    def verificar_login(self):
        """Chamado pelo botão 'Entrar' no arquivo .kv. Se o login for
        bem-sucedido troca para a tela 'main'."""

        usuario_digitado = self.ids.user_input.text
        senha_digitada = self.ids.pass_input.text

        usuarios_cadastrados = {
            "admin": "senha123",
            "usuario": "abc",
            "kivy_dev": "python",
        }

        feedback_label = self.ids.feedback

        if usuario_digitado in usuarios_cadastrados:
            if usuarios_cadastrados[usuario_digitado] == senha_digitada:
                feedback_label.text = f'Login bem-sucedido! Bem-vindo(a), {usuario_digitado}.'
                feedback_label.color = (0, 1, 0, 1)
                # Troca para a tela principal
                if self.manager:
                    self.manager.current = 'main'
            else:
                feedback_label.text = 'Senha incorreta.'
                feedback_label.color = (1, 0, 0, 1)
        else:
            feedback_label.text = 'Usuário não encontrado.'
            feedback_label.color = (1, 0, 0, 1)

        # Limpa o campo de senha após a tentativa
        self.ids.pass_input.text = ""


DEFAULT_COMMAND = os.path.join(os.path.dirname(__file__), 'codigoParaInicar.py')


class MainScreen(Screen):
    """Tela principal que aparece após login bem-sucedido."""

    def run_command(self):
        """Inicia o comando especificado no campo de texto em background.

        Se o campo estiver vazio executa `codigoParaInicar.py` por padrão.
        Usa shell=True para permitir comandos compostos (pipes/redirecionamentos).
        """
        # obtém o comando do campo de texto (se presente)
        cmd_text = ''
        try:
            if 'command_input' in self.ids:
                cmd_text = self.ids.command_input.text.strip()
        except Exception:
            cmd_text = ''

        if not cmd_text:
            cmd_text = f'python "{DEFAULT_COMMAND}"'

        try:
            subprocess.Popen(cmd_text, shell=True)
            if 'main_feedback' in self.ids:
                self.ids.main_feedback.text = f'Comando iniciado.'
        except Exception as e:
            if 'main_feedback' in self.ids:
                self.ids.main_feedback.text = f'Erro ao iniciar: {e}'
            else:
                print(f'Erro ao iniciar comando: {e}')


class PainelApp(App):
    """App principal. Cria um ScreenManager com as telas de login e
    tela principal."""

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

# --- Ponto de entrada do script ---
if __name__ == '__main__':
    PainelApp().run()