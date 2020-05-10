import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, screen, ship, bulletsize=[15,3], color=(60,60,60), speed=1.5, direction=1):
        super(Bullet, self).__init__()
        self.width, self.height = bulletsize
        self.direction = direction
        self.screen = screen
        
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.centery = ship.rect.centery
        self.rect.right = ship.rect.right
        self.x = float(self.rect.x)
        
        self.color = color
        self.speed = speed
    
    def update(self):
        if self.direction == 1: # 1 ====>
            self.x += self.speed
        else:
            self.x -= self.speed
        
        self.rect.x = self.x
    
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)