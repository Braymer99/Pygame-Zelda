# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

#  game setup
WIDTH = 1000
HEIGTH = 600
FPS = 60
TILESISE = 64
# Tamaño del mapa en tiles
MAP_WIDTH = 30   # Ajusta según el tamaño real de tu mapa
MAP_HEIGHT = 20  # Ajusta según el tamaño real de tu mapa

HITBOX_OFFSET = {"player": -26, "object": -40, "grass": -10, "invisible": 0}

# UI
BAR_HEIGHT = 10
HEALTH_BAR_WIDTH = 0
ENERGY_BAR_WIDTH = 0
ITEM_BOX_SIZE = 80
UI_FONT = "assets/fonts/joystix.ttf"
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

# UI colors
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# upgrade menu
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"

# magic
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': 'assets/images/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': 'assets/images/particles/heal/heal.png'}
}

# enemy
monster_data = {
    'squid': {'health': 100, 'exp': 100, 'damage': 30, 'attack_type': 'slash', 'attack_sound': 'assets/sounds/attack/slash.wav', 'speed': 3, 'resistance': 1, 'attack_radius': 60, 'notice_radius': 250},
    'raccoon': {'health': 300, 'exp': 250, 'damage': 60, 'attack_type': 'claw',  'attack_sound': 'assets/sounds/attack/claw.wav', 'speed': 2.5, 'resistance': 2, 'attack_radius': 75, 'notice_radius': 280},
    'spirit': {'health': 100, 'exp': 120, 'damage': 20, 'attack_type': 'thunder', 'attack_sound': 'assets/sounds/attack/fireball.wav', 'speed': 2.8, 'resistance': 1, 'attack_radius': 90, 'notice_radius': 300},
    'bamboo': {'health': 70, 'exp': 120, 'damage': 20, 'attack_type': 'leaf_attack', 'attack_sound': 'assets/sounds/attack/slash.wav', 'speed': 3.2, 'resistance': 1, 'attack_radius': 50, 'notice_radius': 240}
}
