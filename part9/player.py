import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player/down_idle/idle_downOne.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-45,-40)

        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        # движение
        self.direction = pygame.math.Vector2()

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.switch_duration_cooldown = 200

        self.magic_index = 0
        self.magic = list()

        self.stats = {'health':100,'energy':60,'attack':10,'magic':4,'speed':7}
        self.health = self.stats['health'] * 0.7
        self.energy = self.stats['energy'] * 0.9
        self.exp = 100
        self.speed = self.stats['speed']

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        self.animations = {
            'down_idle':[pygame.image.load('graphics/player/down_idle/idle_downOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/down_idle/idle_downTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/down_idle/idle_downThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/down_idle/idle_downFour.png').convert_alpha(),
                     pygame.image.load('graphics/player/down_idle/idle_downFive.png').convert_alpha(),
                     pygame.image.load('graphics/player/down_idle/idle_downSix.png').convert_alpha()],
            'down': [pygame.image.load('graphics/player/down/DownOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/down/DownTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/down/DownThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/down/DownFour.png').convert_alpha(),
                     pygame.image.load('graphics/player/down/DownFive.png').convert_alpha(),
                     pygame.image.load('graphics/player/down/DownSix.png').convert_alpha()],
            'up_idle':[pygame.image.load('graphics/player/up_idle/idle_upOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/up_idle/idle_upTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/up_idle/idle_upThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/up_idle/idle_upFour.png').convert_alpha(),
                     pygame.image.load('graphics/player/up_idle/idle_upFive.png').convert_alpha(),
                     pygame.image.load('graphics/player/up_idle/idle_upSix.png').convert_alpha()],
            'up': [pygame.image.load('graphics/player/up/UpOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/up/UpTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/up/UpThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/up/UpFour.png').convert_alpha(),
                     pygame.image.load('graphics/player/up/UpFive.png').convert_alpha(),
                     pygame.image.load('graphics/player/up/UpSix.png').convert_alpha()],
            'right_idle':[pygame.image.load('graphics/player/right_idle/idle_rightOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/right_idle/idle_rightTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/right_idle/idle_rightThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/right_idle/idle_rightFour.png').convert_alpha(),
                     pygame.image.load('graphics/player/right_idle/idle_rightFive.png').convert_alpha(),
                     pygame.image.load('graphics/player/right_idle/idle_rightSix.png').convert_alpha()],
            'right':[pygame.image.load('graphics/player/right/RightOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/right/RightTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/right/RightThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/right/RightFour.png').convert_alpha(),
                     pygame.image.load('graphics/player/right/RightFive.png').convert_alpha(),
                     pygame.image.load('graphics/player/right/RightSix.png').convert_alpha()],
            'left_idle':[pygame.image.load('graphics/player/left_idle/idle_leftOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/left_idle/idle_leftTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/left_idle/idle_leftThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/left_idle/idle_leftFour.png').convert_alpha(),
                     pygame.image.load('graphics/player/left_idle/idle_leftFive.png').convert_alpha(),
                     pygame.image.load('graphics/player/left_idle/idle_leftSix.png').convert_alpha()],
            'left':[pygame.image.load('graphics/player/left/LeftOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/left/LeftTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/left/LeftThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/left/LeftFour.png').convert_alpha(),
                     pygame.image.load('graphics/player/left/LeftFive.png').convert_alpha(),
                     pygame.image.load('graphics/player/left/LeftSix.png').convert_alpha()],
            'up_attack':[pygame.image.load('graphics/player/attack_up/up_attackOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_up/up_attackTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_up/up_attackThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_up/up_attackFour.png').convert_alpha()],
            'down_attack':[pygame.image.load('graphics/player/attack_down/down_attackOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_down/down_attackTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_down/down_attackThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_down/down_attackFour.png').convert_alpha()],
            'right_attack':[pygame.image.load('graphics/player/attack_right/right_attackOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_right/right_attackTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_right/right_attackThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_right/right_attackFour.png').convert_alpha()],
            'left_attack':[pygame.image.load('graphics/player/attack_left/left_attackOne.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_left/left_attackTwo.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_left/left_attackThree.png').convert_alpha(),
                     pygame.image.load('graphics/player/attack_left/left_attackFour.png').convert_alpha()]
        }

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            mouse_presses = pygame.mouse.get_pressed()

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
    

            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('magic')

            if keys[pygame.K_q] and self.can_switch_magic:
                print('change')
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(self.magic) - 1:
                    self.magic_index += 1
                    # вставить что меняется магия по индексу
                else:
                    self.magic_index = 0

            if mouse_presses[0] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                print('attack')

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # движение вправо
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # движение влево
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # движение вниз
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # движение вверх
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time > self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time > self.switch_duration_cooldown:
                self.can_switch_magic = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        