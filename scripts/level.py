# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from scripts.settings import *
from scripts.tile import Tile
from scripts.player import Player
from scripts.debug import debug
from scripts.support import *
from random import choice, randint
from scripts.ui import UI
from scripts.enemy import Enemy
from scripts.particles import AnimationPlayer
from scripts.magic import MagicPlayer
from scripts.upgrade import Upgrade


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Setup
        self.create_map()
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layouts = {
            "boundary": import_csv_layout("assets/maps/map_FloorBlocks.csv"),
            "grass": import_csv_layout("assets/maps/map_Grass.csv"),
            "object": import_csv_layout("assets/maps/map_Objects.csv"),
            "entities": import_csv_layout("assets/maps/map_Entities.csv"),
        }

        graphics = {
            "grass": import_folder("assets/images/grass"),
            "objects": import_folder("assets/images/objects")
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESISE
                        y = row_index * TILESISE

                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")

                        elif style == "grass":
                            image = choice(graphics["grass"])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], "grass", image)

                        elif style == "object":
                            surface = graphics["objects"][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], "object", surface)

                        elif style == "entities":
                            if col == "394":
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_magic
                                )
                            else:
                                monster_name = {
                                    "390": "bamboo",
                                    "391": "spirit",
                                    "392": "raccoon"
                                }.get(col, "squid")
                                enemy = Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites],
                                              self.obstacle_sprites, self.damage_player, self.trigger_death_particles, self.add_exp)
                                self.enemy_sprites.add(enemy)

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        elif style == "flame":
            self.magic_player.flame(self.player, cost, [self.visible_sprites])

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.get_damage(amount)
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, type_):
        self.animation_player.create_particles(type_, pos, self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def player_attack_logic(self):
        if not self.player.attacking:
            return  # No atacar si no está atacando

        attack_rect = self.player.rect.copy()
        offset = pygame.math.Vector2()
        attack_size = pygame.Rect(0, 0, 40, 40)

        if self.player.status.startswith("right"):
            offset = pygame.math.Vector2(self.player.rect.width, self.player.rect.height // 4)
        elif self.player.status.startswith("left"):
            offset = pygame.math.Vector2(-attack_size.width, self.player.rect.height // 4)
        elif self.player.status.startswith("up"):
            offset = pygame.math.Vector2(self.player.rect.width // 4, -attack_size.height)
        elif self.player.status.startswith("down"):
            offset = pygame.math.Vector2(self.player.rect.width // 4, self.player.rect.height)

        attack_rect.topleft += offset

        damage = self.player.stats["attack"]

        for target in self.attackable_sprites:
            if attack_rect.colliderect(target.rect):
                if target.sprite_type == "grass":
                    pos = target.rect.center
                    offset = pygame.math.Vector2(0, 75)
                    for _ in range(randint(3, 6)):
                        self.animation_player.create_grass_particle(pos - offset, [self.visible_sprites])
                    target.kill()
                else:
                    try:
                        target.get_damage(self.player, damage, "slash")
                    except Exception as e:
                        print(f"Error al aplicar daño a {target}: {e}")

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        # Barra de vida con imagen escalada según vida actual
        health_ratio = self.player.health / self.player.stats["health"]
        health_bar_img = pygame.image.load("assets/ui/energy_bar.png").convert_alpha()
        full_width = health_bar_img.get_width()
        height = health_bar_img.get_height()
        visible_width = int(full_width * health_ratio)
        health_bar_visible = health_bar_img.subsurface((0, 0, visible_width, height))
        self.display_surface.blit(health_bar_visible, (1, 1))

        if self.game_paused:
            self.upgrade.display()
        else:
            for enemy in self.enemy_sprites:
                enemy.enemy_update(self.player)
                enemy.update()
            self.visible_sprites.update()
            self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_heigth = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load("assets/images/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth

        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
