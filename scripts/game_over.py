# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

import pygame
import random
import math
from scripts.settings import WIDTH, HEIGTH


class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        self.max_particles = 80
        self.font_large = pygame.font.Font(None, 120)
        self.font_small = pygame.font.Font(None, 40)
        self.red = (255, 30, 30)  # Rojo brillante y visible
        self.white = (255, 255, 255)
        self.counter = 0  # Para animar texto

        for _ in range(self.max_particles):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGTH)
            speed_y = random.uniform(0.3, 1.2)
            size = random.randint(2, 4)
            self.particles.append([x, y, speed_y, size])

    def update_particles(self):
        for p in self.particles:
            p[1] -= p[2]
            if p[1] < 0:
                p[0] = random.randint(0, WIDTH)
                p[1] = HEIGTH + random.randint(10, 50)
                p[2] = random.uniform(0.3, 1.2)
                p[3] = random.randint(2, 4)

    def draw_particles(self):
        for x, y, _, size in self.particles:
            rect = pygame.Rect(int(x), int(y), size, size)
            pygame.draw.rect(self.screen, self.red, rect)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fondo negro

        self.draw_particles()
        self.update_particles()

        # Texto "GAME OVER" con efecto pulsante
        self.counter += 0.05
        scale = 1 + 0.05 * math.sin(self.counter)
        text_surface = self.font_large.render("GAME OVER", True, self.red)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2))
        scaled_surface = pygame.transform.rotozoom(text_surface, 0, scale)
        scaled_rect = scaled_surface.get_rect(center=text_rect.center)
        self.screen.blit(scaled_surface, scaled_rect)

        # Texto reinicio abajo
        restart_text = self.font_small.render("Presiona R para reiniciar", True, self.white)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGTH // 2 + 100))
        self.screen.blit(restart_text, restart_rect)
