# gamepad.py

import pygame

class Gamepad:
    def __init__(self):
        pygame.joystick.init()
        self.joystick = None
        self.hat_x = 0
        self.hat_y = 0
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"[INFO] Mando conectado: {self.joystick.get_name()}")
        else:
            print("[ERROR] No se detectó ningún mando.")

    def process_event(self, event, game_state):
        """
        Procesa eventos pygame relacionados con el gamepad.
        Devuelve un diccionario con las acciones detectadas:
        - start_pressed: True si se presionó START (botón 7)
        - attack_pressed: True si se presionó O (botón 1)
        - direction: tupla (x, y) de dirección según D-pad o joystick
        - status: string 'up', 'down', 'left', 'right' para animaciones
        """
        actions = {
            "start_pressed": False,
            "attack_pressed": False,
            "direction": (0, 0),
            "status": None,
        }

        START_BUTTON = 7
        ATTACK_BUTTON = 1

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == START_BUTTON:
                if game_state in ['menu', 'game_over']:
                    actions["start_pressed"] = True
            elif game_state == 'playing' and event.button == ATTACK_BUTTON:
                actions["attack_pressed"] = True

        if event.type == pygame.JOYHATMOTION:
            self.hat_x, self.hat_y = event.value
            if game_state == 'playing':
                actions["direction"] = (self.hat_x, -self.hat_y)
                abs_x = abs(self.hat_x)
                abs_y = abs(self.hat_y)
                if abs_x > abs_y:
                    actions["status"] = "right" if self.hat_x > 0 else "left"
                elif abs_y > 0:
                    actions["status"] = "up" if self.hat_y > 0 else "down"

        return actions
