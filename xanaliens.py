import pygame, random
from pygame.sprite import Sprite
import xanbullet

class Alien(Sprite):
    """An Alien Base Class"""
    def __init__(self, screen):
        super(Alien, self).__init__()
        self.screen = screen
        # Load the alien image, and set its rect attribute.
        self.image = pygame.image.load('xanfiles/alienred1.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.boss = False
        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the alien right or left."""
        self.x += (0.5 * -1)
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)


class GreenAlien1(Alien):
    """The most basic alien and first of the green series.
    It moves simply straight down the screen"""
    def __init__(self, screen):
        super(GreenAlien1, self).__init__(screen)
        self.screen = screen
        self.image = pygame.image.load('xanfiles/aliengreen1.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.direction = random.choice([1,-1])
        self.points = 50
        self.boss = False
    
    def update(self):
        """Move the alien"""
        screen_rect = self.screen.get_rect()
        self.x -= 0.4
        self.rect.x = self.x
        self.rect.y = self.y
        if self.rect.right <= screen_rect.left:
            self.kill()


class RedAlien1(Alien):
    """The first alien of the red alien series.
    It bounces off walls as its animation."""
    def __init__(self, screen):
        super(RedAlien1, self).__init__(screen)
        self.screen = screen
        #self.image = self.image = pygame.image.load('xanfiles/alienred1.png')
        self.image = pygame.image.load('xanfiles/alienred1.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.direction = random.choice([1,-1])
        self.points = 50
        self.boss = False
    
    def update(self):
        """Move alien in a random direction definined by __init__
        if touching edge, reverse directon"""
        screen_rect = self.screen.get_rect()
        if self.rect.top <= screen_rect.top:
            self.direction = 1
            self.y += 0.3
        elif self.rect.bottom >= screen_rect.bottom-50:
            self.direction = -1
            self.y -= 0.3
        self.x -= 0.5
        self.y += 0.3 * self.direction
        self.rect.x = self.x
        self.rect.y = self.y

class BlueAlien1(Alien):
    """The first alien of the blue alien series.
    It shoots forward if the ship is underneath."""
    def __init__(self, screen, player):
        super(BlueAlien1, self).__init__(screen)
        self.screen = screen
        self.player = player
        #self.image = self.image = pygame.image.load('xanfiles/alienred1.png')
        self.image = pygame.image.load('xanfiles/alienblue1.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.movingdown = False
        self.direction = random.choice([1,-1])
        self.points = 75
        self.boss = False
    
    def update(self):
        """Move alien in a random direction definined by __init__
        if touching edge, reverse directon. If ship is beneath, speed."""
        if self.player.rect.y < self.rect.y+5 and self.player.rect.y > self.rect.y-5:
            self.movingdown = True
            self.x -= 10
        elif self.movingdown == True:
            self.x -= 10
        else:
            screen_rect = self.screen.get_rect()
            if self.rect.top <= screen_rect.top:
                self.direction = 1
                self.y += 0.3
            elif self.rect.bottom >= screen_rect.bottom - 50:
                self.direction = -1
                self.y -= 0.3
                self.y += 0.3 * self.direction
            else:
                self.y += 0.3 * self.direction
        self.rect.x = self.x
        self.rect.y = self.y

class BossAlien1(Alien):
    """The first alien of the blue alien series.
    It shoots forward if the ship is underneath."""
    def __init__(self, screen, player):
        super(BossAlien1, self).__init__(screen)
        self.screen = screen
        self.player = player
        self.image = pygame.image.load('xanfiles/alienboss1.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.direction = random.choice([1,-1])
        self.health = 50
        self.points = 500
        self.shotcounter = 0
        self.boss = True
    
    def update(self):
        """Move alien in a random direction definined by __init__
        if touching edge, reverse directon.
        Return bullets"""
        screen_rect = self.screen.get_rect()
        if self.rect.top <= screen_rect.top:
            self.direction = 1
            self.y += 0.3
        elif self.rect.bottom >= screen_rect.bottom - 50:
            self.direction = -1
            self.y -= 0.3
            self.y += 0.3 * self.direction
        else:
            self.y += 0.3 * self.direction
        self.rect.x = self.x
        self.rect.y = self.y
        self.fire()
    
    def fire(self):
        self.shotcounter += 1
        if self.shotcounter > 150:
            self.shotcounter = 0
            print("shot")
            new1 = xanbullet.Bullet(self.screen, self, direction=-1)
            new1.rect.centery = self.rect.top + 9
            new1.rect.right -= 40
            new2 = xanbullet.Bullet(self.screen, self, direction=-1)
            new2.rect.centery = self.rect.top + 88
            new2.rect.right -= 40
            return [new1, new2]
        else:
            return []
    
    def hit(self):
        if self.health <= 0:
            self.dead = True
        else:
            self.health -= 1
            self.dead = False
        print(self.health, self.dead)
        return self.dead


class RedAlien2(Alien):
    """The first alien of the red alien series.
    It bounces off walls faster than the first."""
    def __init__(self, screen):
        super(RedAlien2, self).__init__(screen)
        self.screen = screen
        self.image = pygame.image.load('xanfiles/alienred2.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.direction = random.choice([1,-1])
        self.points = 75
        self.boss = False
    
    def update(self):
        """Move alien in a random direction definined by __init__
        if touching edge, reverse directon"""
        screen_rect = self.screen.get_rect()
        if self.rect.top <= screen_rect.top:
            self.direction = 1
            self.y += 0.4
        elif self.rect.bottom >= screen_rect.bottom-50:
            self.direction = -1
            self.y -= 0.4
        self.x -= 1
        self.y += 0.4 * self.direction
        self.rect.x = self.x
        self.rect.y = self.y

class GreenAlien2(Alien):
    """The second of the green series.
    It moves faster straight down the screen"""
    def __init__(self, screen):
        super(GreenAlien2, self).__init__(screen)
        self.screen = screen
        self.image = pygame.image.load('xanfiles/aliengreen2.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.direction = random.choice([1,-1])
        self.points = 50
        self.boss = False
    
    def update(self):
        """Move the alien"""
        screen_rect = self.screen.get_rect()
        self.x -= 1
        self.rect.x = self.x
        self.rect.y = self.y
        if self.rect.right <= screen_rect.left:
            self.kill()



if __name__ == "__main__":
    help(BossAlien1)