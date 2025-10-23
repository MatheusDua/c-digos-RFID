import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import subprocess
import shlex
import os
import sys

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
        Usa shell=True para permitir comandos compostos (pipes/redirecionamentos)
        quando o usuário digitar algo.
        """
        cmd_text = ''
        try:
            if 'command_input' in self.ids:
                cmd_text = self.ids.command_input.text.strip()
        except Exception:
            cmd_text = ''

        if not cmd_text:
            # usa o python do ambiente atual para executar o script padrão
            cmd = [sys.executable, DEFAULT_COMMAND]
        else:
            # se o usuário digitou algo, permite comandos compostos via shell
            cmd = cmd_text

        try:
            if isinstance(cmd, (list, tuple)):
                subprocess.Popen(cmd)
            else:
                subprocess.Popen(cmd, shell=