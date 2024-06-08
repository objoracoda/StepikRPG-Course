import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface=pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'house':
            self.rect = self.image.get_rect(topleft=(pos[0],pos[1]-TILESIZE*4))
            self.hitbox = self.rect.inflate(-50,-100)
        elif sprite_type == 'tree':
            self.rect = self.image.get_rect(topleft=(pos[0]-TILESIZE-(TILESIZE//2),pos[1]-TILESIZE*4))
            self.hitbox = self.rect.inflate(-100,-80)
        elif sprite_type == 'invisible':
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0,20)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0,-10)