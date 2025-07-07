# Nombre/Apellido: Braymer David Domínguez Morales
# Matricula: 22-SISN-2-052

import pygame
from scripts.settings import *
from scripts.entity import Entity
from scripts.support import *
from scripts.behavior_tree import Selector, Sequence, Condition, Task, NodeStatus
from scripts.pathfinding import a_star


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):
        super().__init__(groups)
        self.sprite_type = "enemy"

        # Inicializa referencia al jugador para el árbol de comportamiento
        self.player_ref = None

        # Árbol de comportamiento
        self.behavior_tree = self.create_behavior_tree()

        # Gráficos
        self.import_graphics(monster_name)
        self.status = "idle"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.status][self.frame_index]

        # Movimiento
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2()

        # Estadísticas
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.attack_type = monster_info["attack_type"]

        # Interacción con el jugador
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # Invulnerabilidad
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        # Sonidos
        self.death_sound = pygame.mixer.Sound("assets/sounds/death.wav")
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
        self.attack_sound = pygame.mixer.Sound(monster_info["attack_sound"])
        for sound in [self.death_sound, self.hit_sound, self.attack_sound]:
            sound.set_volume(0.6)

    def import_graphics(self, name):
        self.animations = {"idle": [], "move": [], "attack": []}
        main_path = f"assets/images/monsters/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
        if not self.animations["idle"]:
            raise ValueError(f"No se encontraron sprites 'idle' en {main_path}idle")

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        direction = (player_vec - enemy_vec).normalize() if distance > 0 else pygame.math.Vector2()
        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack and self.attack_time:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable and self.hit_time:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, amount, attack_type):
        valid_attack_types = ['weapon', 'slash']
        if self.vulnerable and attack_type in valid_attack_types:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -= amount
            print(f"Enemigo recibe daño: {amount} de tipo {attack_type} de {player}")
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
        

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                    self.rect.centerx = self.hitbox.centerx
                elif direction == "vertical":
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom
                    self.rect.centery = self.hitbox.centery

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()

    def enemy_update(self, player):
        self.player_ref = player
        if hasattr(self, 'behavior_tree'):
            if not hasattr(self, 'last_action_log'):
                self.last_action_log = ""

            import sys
            from io import StringIO

            original_stdout = sys.stdout
            sys.stdout = temp_stdout = StringIO()

            self.behavior_tree.run()

            sys.stdout = original_stdout
            output = temp_stdout.getvalue()

            if output.strip() and output.strip() != self.last_action_log:
                print(output.strip())
                self.last_action_log = output.strip()

    def create_behavior_tree(self):
        def is_player_in_attack_range():
            distance, _ = self.get_player_distance_direction(self.player_ref)
            return distance <= self.attack_radius

        def attack_player():
            if self.can_attack:
                print("[Árbol de comportamiento] Ejecutando tarea: atacar")
                self.attack_time = pygame.time.get_ticks()
                self.damage_player(self.attack_damage, self.attack_type)
                self.attack_sound.play()
                self.can_attack = False
                return NodeStatus.SUCCESS
            return NodeStatus.FAILURE

        def is_player_near():
            distance, _ = self.get_player_distance_direction(self.player_ref)
            return distance <= self.notice_radius

        def move_towards_player():
            start = (self.rect.centerx // TILESISE, self.rect.centery // TILESISE)
            goal = (self.player_ref.rect.centerx // TILESISE, self.player_ref.rect.centery // TILESISE)
            path = a_star(start, goal, self.obstacle_sprites)
            if path:
              next_node = path[0]
              target_pos = pygame.Vector2(next_node[0] * TILESISE, next_node[1] * TILESISE)
              self.direction = (target_pos - pygame.Vector2(self.rect.center)).normalize()
              print(f"[A*] Camino calculado: {path}")
              return NodeStatus.SUCCESS
            else:
             print("[A*] No se encontró un camino")
            return NodeStatus.FAILURE


        return Selector([
            Sequence([
                Condition(is_player_in_attack_range),
                Task(attack_player)
            ]),
            Sequence([
                Condition(is_player_near),
                Task(move_towards_player)
            ])
        ])
