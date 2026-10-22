from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

player = None
ground = None
labirinto_entidades = []
chegada = None
jogo_ativo = False 

# ==========================================
# 1. LÓGICA DO JOGO (LABIRINTO)
# ==========================================
sky = Sky()
sky.color = color.blue

def criar_labirinto():
    global chegada
    labirinto = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    ]
    
    block_size = 2
    
    for z, row in enumerate(labirinto):
        for x, cell in enumerate(row):
            if cell == 1:
                parede = Entity(
                    model='cube', 
                    texture="brick", 
                    scale=(block_size, 5, block_size),
                    color=color.gray,
                    position=(x * block_size, 2.5, z * block_size), 
                    collider='box'
                )
                labirinto_entidades.append(parede)
            
            # A saída está na linha 14, coluna 13
            elif cell == 0 and x == 13 and z == 14:
                chegada = Entity(
                    model='cube',
                    scale=(block_size, 0.1, block_size),
                    color=color.gold,
                    position=(x * block_size, 0.1, z * block_size),
                )
                # Adiciona um texto flutuante em cima da saída para ficar visível
                Text(
                    text='SAÍDA',
                    position=(x * block_size, 2, z * block_size),
                    scale=10,
                    color=color.gold,
                    billboard=True, # Sempre olha para a câmera
                    origin=(0,0)
                )

# ==========================================
# 2. FUNÇÕES DO JOGO
# ==========================================
def iniciar_jogo():
    global player, ground, chegada, jogo_ativo
    
    menu_ui.enabled = False
    tela_vitoria.enabled = False
    mouse.locked = True
    jogo_ativo = True
    
    ground = Entity(
        model='plane',
        scale=(1000, 1, 1000),
        texture='grass',
        texture_scale=(10, 10),
        collider='box'
    )
    
    player = FirstPersonController(
        mouse_sensitivity=Vec2(100, 100),
        position=(2, 2, 2) 
    )
    player.speed = 10 
    player.jump_height = 2.5  
    
    criar_labirinto()

def voltar_ao_menu():
    global player, ground, jogo_ativo
    jogo_ativo = False
    
    if player: destroy(player)
    if ground: destroy(ground)
    if chegada: destroy(chegada)
    
    for parede in labirinto_entidades:
        destroy(parede)
    labirinto_entidades.clear()
    
    menu_ui.enabled = True
    tela_vitoria.enabled = False
    mouse.locked = False

def sair_do_jogo():
    application.quit()

# ==========================================
# 3. CRIAÇÃO DA INTERFACE DO MENU (UI)
# ==========================================
menu_ui = Entity(parent=camera.ui)
fundo = Entity(parent=menu_ui, model='quad', scale=(2, 1), color=color.black66)

titulo = Text(
    parent=menu_ui, 
    text='LABIRINTO 3D', 
    y=0.3, 
    origin=(0, 0), 
    scale=3, 
    color=color.white
)

Button(
    parent=menu_ui,
    text='JOGAR',
    scale=(0.3, 0.1),
    y=0,
    color=color.dark_gray,
    highlight_color=color.gray,
    on_click=iniciar_jogo
)

Button(
    parent=menu_ui,
    text='SAIR',
    scale=(0.3, 0.1),
    y=-0.15,
    color=color.dark_gray,
    highlight_color=color.gray,
    on_click=sair_do_jogo
)

tela_vitoria = Entity(parent=camera.ui, enabled=False)
Entity(parent=tela_vitoria, model='quad', scale=(2, 1), color=color.black90)
Text(parent=tela_vitoria, text='VOCÊ VENCEU!', y=0.1, origin=(0, 0), scale=3, color=color.yellow)

Button(
    parent=tela_vitoria,
    text='Voltar ao Menu',
    scale=(0.3, 0.1),
    y=-0.1,
    color=color.dark_gray,
    highlight_color=color.gray,
    on_click=voltar_ao_menu
)

# ==========================================
# 4. CONTROLE DE TECLAS E COLISÕES (UPDATE)
# ==========================================
def update():
    global jogo_ativo
    
    if player and held_keys['escape']:
        voltar_ao_menu()
    
    # NOVA LÓGICA DE VITÓRIA: verifica a distância entre jogador e saída
    if jogo_ativo and player and chegada:
        distancia = distance(player.position, chegada.position)
        if distancia < 3:  # Se o jogador chegar a menos de 3 metros da saída
            jogo_ativo = False
            mouse.locked = False
            tela_vitoria.enabled = True 

mouse.locked = False 
app.run()