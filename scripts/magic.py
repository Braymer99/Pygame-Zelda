# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

import pygame
from scripts.settings import *
from random import randint


class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            "heal": pygame.mixer.Sound("assets/sounds/heal.wav"),
            "flame": pygame.mixer.Sound("assets/sounds/fire.wav")
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds["heal"].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]

            self.animation_player.create_particles("aura", player.rect.center, groups)
            self.animation_player.create_particles("heal", player.rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds["flame"].play()

            status_direction = player.status.split("_")[0]
            direction = {
                "right": pygame.math.Vector2(1, 0),
                "left": pygame.math.Vector2(-1, 0),
                "up": pygame.math.Vector2(0, -1),
                "down": pygame.math.Vector2(0, 1)
            }.get(status_direction, pygame.math.Vector2(0, 1))

            for i in range(1, 6):
                offset = direction * i * TILESISE
                x = player.rect.centerx + (offset.x if direction.x else randint(-TILESISE // 3, TILESISE // 3))
                y = player.rect.centery + (offset.y if direction.y else randint(-TILESISE // 3, TILESISE // 3))
                self.animation_player.create_particles("flame", (x, y), groups)
