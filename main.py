# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

import pygame
import sys
from scripts.settings import *
from scripts.level import Level
from scripts.menu import Menu
from scripts.game_over import GameOverScreen

class Game:
    def __init__(self):
        pygame.init()
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

        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Zelda')
        logo = pygame.image.load('assets/images/logo/Zelda.png')
        pygame.display.set_icon(logo)
        self.clock = pygame.time.Clock()

        self.state = 'menu'
        self.level = None
        self.menu = Menu(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)

        self.font = pygame.font.Font(None, 50)
        self.retry_text = self.font.render("Presiona R para reiniciar", True, (255, 255, 255))
        self.retry_rect = self.retry_text.get_rect(center=(WIDTH//2, HEIGTH//2 + 100))

        self.main_sound = pygame.mixer.Sound("assets/music/zelda.mp3")
        self.main_sound.set_volume(0.5)
        self.main_sound.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Teclado intacto
                if event.type == pygame.KEYDOWN:
                    if self.state == 'menu' and event.key == pygame.K_RETURN:
                        self.level = Level()
                        self.state = 'playing'
                    elif self.state == 'game_over' and event.key == pygame.K_r:
                        self.level = Level()
                        self.state = 'playing'

                # Botones mando
                if event.type == pygame.JOYBUTTONDOWN:
                    print(f"[JOY] Botón presionado: {event.button}")
                    if event.button == 7:  # START
                        if self.state == 'menu':
                            self.level = Level()
                            self.state = 'playing'
                        elif self.state == 'game_over':
                            self.level = Level()
                            self.state = 'playing'
                    elif self.state == 'playing' and event.button == 1:  # O para atacar
                        if self.level and self.level.player:
                            self.level.player.trigger_attack()

                # D-pad (hat) mando
                if event.type == pygame.JOYHATMOTION:
                    self.hat_x, self.hat_y = event.value
                    if self.state == 'playing' and self.level and self.level.player:
                        self.level.player.direction.x = self.hat_x
                        self.level.player.direction.y = -self.hat_y  # invertir eje Y para que coincida con teclado

                        abs_x = abs(self.hat_x)
                        abs_y = abs(self.hat_y)
                        if abs_x > abs_y:
                            self.level.player.status = "right" if self.hat_x > 0 else "left"
                        elif abs_y > 0:
                            self.level.player.status = "up" if self.hat_y > 0 else "down"
                        else:
                            if "idle" not in self.level.player.status and "attack" not in self.level.player.status:
                                self.level.player.status += "_idle"

            # Movimiento joystick analógico ejes 0 y 1
            if self.state == 'playing' and self.joystick and self.level and self.level.player:
                axis_x = self.joystick.get_axis(0)
                axis_y = self.joystick.get_axis(1)

                threshold = 0.1
                move_x = axis_x if abs(axis_x) > threshold else 0
                move_y = axis_y if abs(axis_y) > threshold else 0

                if move_x != 0 or move_y != 0:
                    self.level.player.direction.x = move_x
                    self.level.player.direction.y = move_y

                    abs_x = abs(move_x)
                    abs_y = abs(move_y)
                    if abs_x > abs_y:
                        self.level.player.status = "right" if move_x > 0 else "left"
                    elif abs_y > 0:
                        self.level.player.status = "down" if move_y > 0 else "up"
                    else:
                        if "idle" not in self.level.player.status and "attack" not in self.level.player.status:
                            self.level.player.status += "_idle"

                else:
                    if self.hat_x == 0 and self.hat_y == 0:
                        self.level.player.direction.x = 0
                        self.level.player.direction.y = 0
                        if not self.level.player.attacking:
                            if "idle" not in self.level.player.status and "attack" not in self.level.player.status:
                                self.level.player.status += "_idle"

            # Fondo según estado
            if self.state in ['menu', 'playing']:
                self.screen.fill(WATER_COLOR)

            if self.state == 'menu':
                self.menu.draw()

            elif self.state == 'playing':
                if self.level:
                    self.level.run()
                    if self.level.player.health <= 0:
                        self.state = 'game_over'
                else:
                    self.state = 'menu'

            elif self.state == 'game_over':
                self.game_over_screen.draw()

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
