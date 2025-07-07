# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

import pygame
from scripts.settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Rectángulo de la barra de vida (se queda como antes)
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)

        # Cargar y escalar la imagen de la barra de energía (más grande)
        # Cargar y escalar la imagen al mismo tamaño que la barra original
        self.energy_bar_image = pygame.image.load("assets/ui/energy_bar.png").convert_alpha()
        # Ajusta el tamaño deseado multiplicando por 2 (o el factor que prefieras)
        self.energy_bar_image = pygame.transform.scale(
            self.energy_bar_image,
            (ENERGY_BAR_WIDTH * 2, BAR_HEIGHT * 2)
        )
        self.energy_bar_width = ENERGY_BAR_WIDTH * 2
        self.energy_bar_height = BAR_HEIGHT * 2
        
        # Ajusta la posición según el nuevo tamaño
        self.energy_bar_pos = (1, 1)  # O mueve esta posición para que no se superponga


    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_energy_bar_image(self, current, max_value):
        ratio = current / max_value
        current_width = int(self.energy_bar_width * ratio)

        if current_width > 0:
            cropped_image = self.energy_bar_image.subsurface((0, 0, current_width, self.energy_bar_height))
            self.display_surface.blit(cropped_image, self.energy_bar_pos)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(15, 15))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(15, 15), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        border_color = UI_BORDER_COLOR_ACTIVE if has_switched else UI_BORDER_COLOR
        pygame.draw.rect(self.display_surface, border_color, bg_rect, 3)
        return bg_rect

    
    def display(self, player):
        self.show_energy_bar_image(player.energy, player.stats["energy"])  # Usa imagen en vez de rectángulo
        self.show_exp(player.exp)
       # self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
