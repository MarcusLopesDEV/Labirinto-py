import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation

class MenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        
        self.orientation = "vertical"
        # Configuração da cor de fundo
        Window.clearcolor = (0.044, 0.024, 0.072)
        
        # Título do jogo com animação de entrada
        label = Label(text="Running Rooms", font_size=50, size_hint_y=0.2, opacity=0)
        anim_label = Animation(opacity=1, duration=1)
        anim_label.start(label)
        
        # Layout para os botões com animação de entrada
        buttons_layout = BoxLayout(orientation='vertical', size_hint_y=0.7, opacity=0)
        anim_buttons = Animation(opacity=1, duration=1)
        anim_buttons.start(buttons_layout)
        
        # Botão "Play" com animação de entrada
        button1 = Button(text="Play", size_hint=(None, None), size=(400, 80), pos_hint={"center_x": 0.5}, opacity=0)
        button1.bind(on_press=self.opcao1)
        anim_button1 = Animation(opacity=1, duration=1)
        anim_button1.start(button1)
        
        # Botão "Exit" com animação de entrada
        button3 = Button(text="Exit", size_hint=(None, None), size=(400, 80), pos_hint={"center_x": 0.5}, opacity=0)
        button3.bind(on_press=self.sair)
        anim_button3 = Animation(opacity=1, duration=1)
        anim_button3.start(button3)
        
        # Adiciona os widgets ao MenuScreen
        self.add_widget(label)
        self.add_widget(buttons_layout)
        buttons_layout.add_widget(button1)
        buttons_layout.add_widget(button3)
        
        self.process = None  # Armazena uma referência para o processo

    def opcao1(self, instance):
        print("Loading...")
        # Inicia o processo
        try:
            self.process = subprocess.Popen(["python","main.py"])
        except FileNotFoundError:
            print("Arquivo não encontrado.")
  
    def sair(self, instance):
        print("Saindo do aplicativo.")
        if self.process is not None:
            self.process.terminate()  # Encerra o processo se existir
        # Animação de saída
        anim = Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=lambda *args: App.get_running_app().stop())
        anim.start(self)


class MenuApp(App):
    def build(self):
        return MenuScreen()


if __name__ == '__main__':
    MenuApp().run()
