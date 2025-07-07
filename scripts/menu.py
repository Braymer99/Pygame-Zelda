# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

import pygame
import random
from scripts.settings import WIDTH, HEIGTH

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.TILE_SIZE = 32

        # Colores base
        self.colors = {
            'green_light': (106, 190, 48),
            'green_mid': (85, 160, 40),
            'green_dark': (65, 120, 30),
            'bright_green': (150, 255, 100),
            'brown_light': (150, 111, 51),
            'brown_dark': (100, 73, 30)
        }

        # Generar posiciones aleatorias para destellos
        self.flash_points = []
        total_flashes = 120
        for _ in range(total_flashes):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGTH)
            self.flash_points.append([x, y, random.choice([True, False])])  # (x, y, visible)

    def draw_tile(self, x, y, color):
        rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def draw_background(self):
        rows = HEIGTH // self.TILE_SIZE + 1
        cols = WIDTH // self.TILE_SIZE + 1

        for row in range(rows):
            for col in range(cols):
                # Patrón mosaico con tonos verde claro y medio
                color = self.colors['green_light'] if (row + col) % 2 == 0 else self.colors['green_mid']
                self.draw_tile(col * self.TILE_SIZE, row * self.TILE_SIZE, color)

                # Añadir manchas verdes oscuras para textura
                if random.random() < 0.15:
                    self.draw_tile(col * self.TILE_SIZE, row * self.TILE_SIZE, self.colors['green_dark'])

                # Añadir pequeñas manchas marrones dispersas
                if (row * col) % 10 == 0:
                    brown_rect = pygame.Rect(
                        col * self.TILE_SIZE + self.TILE_SIZE // 4,
                        row * self.TILE_SIZE + self.TILE_SIZE // 4,
                        self.TILE_SIZE // 2,
                        self.TILE_SIZE // 2
                    )
                    pygame.draw.rect(self.screen, self.colors['brown_light'], brown_rect)

    def draw_flashes(self):
        for i, (x, y, visible) in enumerate(self.flash_points):
            if visible:
                pygame.draw.rect(self.screen, self.colors['bright_green'], pygame.Rect(x, y, 2, 2))
            # Parpadeo aleatorio para animar
            if random.random() < 0.05:
                self.flash_points[i][2] = not visible

    def update_flashes(self):
        # Movimiento sutil para los destellos
        for i, (x, y, visible) in enumerate(self.flash_points):
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            nx = max(0, min(WIDTH, x + dx))
            ny = max(0, min(HEIGTH, y + dy))
            self.flash_points[i][0] = nx
            self.flash_points[i][1] = ny

    def draw(self):
        self.draw_background()
        self.draw_flashes()
        self.update_flashes()

        # Texto central para iniciar
        font = pygame.font.Font(None, 60)
        text = font.render("PUSH START BUTTON", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGTH // 2))
        self.screen.blit(text, text_rect)
