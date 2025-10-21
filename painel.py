import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

# Define uma cor de fundo (opcional)
Window.clearcolor = (0.15, 0.15, 0.15, 1)

class LoginScreen(BoxLayout):
    """
    Widget raiz da tela. A interface (layout) é definida em 'painel.kv'.
    A lógica (funções/métodos) é definida aqui.
    """

    # --- A FUNÇÃO DE LÓGICA ---
    def verificar_login(self):
        """
        Esta função é chamada pelo arquivo .kv quando o botão é pressionado.
        """
        
        # 1. Pegar os valores dos inputs.
        # Usamos 'self.ids' para acessar os widgets definidos com 'id' no .kv
        usuario_digitado = self.ids.user_input.text
        senha_digitada = self.ids.pass_input.text

        # 2. "Banco de dados" simulado
        usuarios_cadastrados = {
            "admin": "senha123",
            "usuario": "abc",
            "kivy_dev": "python"
        }

        # 3. Lógica de verificação e feedback
        
        # Pega o widget do label de feedback pelo seu id
        feedback_label = self.ids.feedback 

        if usuario_digitado in usuarios_cadastrados:
            if usuarios_cadastrados[usuario_digitado] == senha_digitada:
                # SUCESSO
                feedback_label.text = f'Login bem-sucedido! Bem-vindo(a), {usuario_digitado}.'
                feedback_label.color = (0, 1, 0, 1) # Verde
            else:
                # FALHA (Senha errada)
                feedback_label.text = 'Senha incorreta.'
                feedback_label.color = (1, 0, 0, 1) # Vermelho
        else:
            # FALHA (Usuário não existe)
            feedback_label.text = 'Usuário não encontrado.'
            feedback_label.color = (1, 0, 0, 1) # Vermelho
        
        # Limpa o campo de senha após a tentativa
        self.ids.pass_input.text = ""


class PainelApp(App):
    """
    Classe principal da Aplicação.
    Por convenção do Kivy, se a classe se chama 'PainelApp',
    ela irá carregar automaticamente o arquivo 'painel.kv'.
    """
    def build(self):
        # O método build retorna a instância da classe que o
        # arquivo 'painel.kv' irá estilizar.
        return LoginScreen()

# --- Ponto de entrada do script ---
if __name__ == '__main__':
    PainelApp().run()