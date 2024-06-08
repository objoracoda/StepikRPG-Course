import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon

class Level:
    def __init__(self):
        # получаем текущий экран
        self.display_surface = pygame.display.get_surface()

        # группа спрайтов
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None

        # создание карты
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/mapFloor_FloorBlock.csv'),
            'house': import_csv_layout('map/mapFloor_House.csv'),
            'tree': import_csv_layout('map/mapFloor_Tree.csv')
        }
        graphics = {
            'house': pygame.image.load('graphics/home/home.png').convert_alpha(),
            'tree': [pygame.image.load('graphics/tree/treeRedProp.png').convert_alpha(),
                     pygame.image.load('graphics/tree/treeYellowOne.png').convert_alpha()]
        }
        print(graphics)

        for style, layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'house':
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'house',graphics['house'])
                        if style == 'tree':
                            tree_choice = choice(graphics['tree'])
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'tree',tree_choice)

        self.player = Player((440,460), [self.visible_sprites], self.obstacle_sprites,self.create_attack, self.destroy_attack)
                    
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.create_attack = None

    def run(self):
        # обновление и отрисовка игры
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

        debug(self.player.status)
    

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # основные методы
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        # создание пола
        self.floor_surf = pygame.image.load('graphics/map/mapFloor.png').convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_position)

    