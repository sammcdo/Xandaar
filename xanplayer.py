import pygame

class Ship():
    def __init__(self, screen):
        self.screen = screen
        
        self.image = pygame.image.load("xanfiles/playership.png")
        #self.image.rotate()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.left + 25
        self.rect.y = self.screen_rect.centery
        self.center = float(self.rect.centery)
        print(self.image)
        
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        speed = 1.5
    
    def update(self):
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.center -= 1
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom-50:
            self.center += 1
        self.rect.centery = self.center
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)