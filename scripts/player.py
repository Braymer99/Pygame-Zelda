# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

from typing import Any
import pygame
from scripts.settings import *
from scripts.support import import_folder
from scripts.entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load("assets/images/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["player"])

        # gráficos
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # movimiento
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 200
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # magia
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.switch_duration_cooldown = 200

        # estadísticas
        self.stats = {"health": 100, "energy": 60,
                      "attack": 10, "magic": 4, "speed": 6}
        self.max_stats = {"health": 300, "energy": 140,
                          "attack": 20, "magic": 10, "speed": 10}
        self.upgrade_cost = {"health": 100, "energy": 100,
                             "attack": 100, "magic": 100, "speed": 100}
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 0
        self.speed = self.stats["speed"]

        # daño
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # sonido ataque
        self.weapon_attack_sound = pygame.mixer.Sound("assets/sounds/sword.wav")
        self.weapon_attack_sound.set_volume(0.4)

        # Inicializar joystick
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def import_player_assets(self):
        character_path = "assets/images/player/"
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
            "right_attack": [], "left_attack": [], "up_attack": [], "down_attack": []
        }

        scale_size = (int(TILESISE * 1.0), int(TILESISE * 1.0))

        for animation in self.animations.keys():
            frames = import_folder(character_path + animation)
            scaled_frames = [pygame.transform.scale(frame, scale_size) for frame in frames]
            self.animations[animation] = scaled_frames

    def input(self):
        if not self.attacking:
            self.direction = pygame.math.Vector2(0, 0)

            joystick_active = False

            if self.joystick:
                # Movimiento con joystick analógico
                x_axis = self.joystick.get_axis(0)
                y_axis = self.joystick.get_axis(1)

                if abs(x_axis) > 0.2 or abs(y_axis) > 0.2:
                    self.direction.x = x_axis
                    self.direction.y = y_axis

                    if abs(x_axis) > abs(y_axis):
                        self.status = "right" if x_axis > 0 else "left"
                    else:
                        self.status = "down" if y_axis > 0 else "up"

                    joystick_active = True

                # Movimiento con D-pad (hat)
                hat_x, hat_y = self.joystick.get_hat(0)
                if hat_x != 0 or hat_y != 0:
                    self.direction.x = hat_x
                    self.direction.y = -hat_y  # Y invertida para hats

                    if abs(hat_x) > abs(hat_y):
                        self.status = "right" if hat_x > 0 else "left"
                    else:
                        self.status = "down" if hat_y < 0 else "up"

                    joystick_active = True

                # Ataque solo botón O (botón 1)
                if self.joystick.get_button(1):
                    self.trigger_attack()

                # Magia botón 2 (triángulo)
                if self.joystick.get_button(2):
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    style = list(magic_data.keys())[self.magic_index]
                    strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                    cost = list(magic_data.values())[self.magic_index]["cost"]
                    self.create_magic(style, strength, cost)

                # Cambio magia botón 4 (L1)
                if self.joystick.get_button(4) and self.can_switch_magic:
                    self.can_switch_magic = False
                    self.magic_switch_time = pygame.time.get_ticks()
                    self.magic_index = (self.magic_index + 1) % len(magic_data)
                    self.magic = list(magic_data.keys())[self.magic_index]

            if not joystick_active:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.direction.y = -1
                    self.status = "up"
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.direction.y = 1
                    self.status = "down"
                else:
                    self.direction.y = 0

                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.direction.x = 1
                    self.status = "right"
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.direction.x = -1
                    self.status = "left"
                else:
                    self.direction.x = 0

                if keys[pygame.K_SPACE]:
                    self.trigger_attack()

                if keys[pygame.K_LCTRL]:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    style = list(magic_data.keys())[self.magic_index]
                    strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                    cost = list(magic_data.values())[self.magic_index]["cost"]
                    self.create_magic(style, strength, cost)

                if keys[pygame.K_e] and self.can_switch_magic:
                    self.can_switch_magic = False
                    self.magic_switch_time = pygame.time.get_ticks()
                    self.magic_index = (self.magic_index + 1) % len(magic_data)
                    self.magic = list(magic_data.keys())[self.magic_index]

    def trigger_attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.status = self.status.split("_")[0] + "_attack"
            self.weapon_attack_sound.play()

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if "idle" not in self.status and "attack" not in self.status:
                self.status += "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if "attack" not in self.status:
                self.status = self.status.replace("_idle", "_attack") if "idle" in self.status else self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking and self.attack_time is not None and \
           current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False

        if not self.can_switch_magic and self.magic_switch_time is not None and \
           current_time - self.magic_switch_time >= self.switch_duration_cooldown:
            self.can_switch_magic = True

        if not self.vulnerable and self.hurt_time is not None and \
           current_time - self.hurt_time >= self.invulnerability_duration:
            self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        self.image.set_alpha(self.wave_value() if not self.vulnerable else 255)

    def get_full_weapon_damage(self):
        base_attack = self.stats.get("attack", 0)
        weapon_damage = 0
        return base_attack + weapon_damage

    def get_full_magic_damage(self):
        return self.stats["magic"] + magic_data[self.magic]["strength"]

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats["speed"])
        self.energy_recovery()

    def get_damage(self, amount):
        if self.vulnerable:
            self.health -= amount
            self.hurt_time = pygame.time.get_ticks()
            self.vulnerable = False
            if self.health < 0:
                self.health = 0
            print(f"Daño recibido: {amount}, vida actual: {self.health}")
