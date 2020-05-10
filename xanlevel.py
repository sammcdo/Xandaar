import pygame, sys, json, time
from pygame.sprite import Group
#import pygameMenu
#from pygameMenu.locals import *
import xanplayer
import xanbullet
import xanaliens
import time

"""
Version 1.0: Just a class
Version 1.5: Ship moves
Version 2.0: Uses level files
Version 2.5: Uses Joystick (1st on arcade)
V 2.6: Hides mouse if joystick
V 2.7: Kills all aliens w/i 100 px of edge b/c if not ship loses all lives
"""


def checkkeydown(event, ship, bullets, screen):
    if event.key == pygame.K_UP:
        ship.moving_up = True                
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_SPACE:
        if len(bullets) < 10:
            new = xanbullet.Bullet(screen, ship)
            bullets.add(new)

def checkkeyup(event, ship, menu):
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_p:
        menu()
    """
        if menu.is_enabled() == True:
            menu.disable()
            print("disabled")
        else:
            menu.enable()
            menu.draw()
            print("enabled")"""
        
wasdown = False

def checkjoystickevents(event, ship, bullets, screen, j1, j2):
    global wasdown
    if j1.get_axis(1) >= 0.5:
        ship.moving_down = True
    elif j1.get_axis(1) <= -0.5:
        ship.moving_up = True
    else:
        ship.moving_down = False
        ship.moving_up = False
    
    if j1.get_button(6) == 0 and wasdown == True:
        wasdown=False
        if len(bullets) < 10:
            new = xanbullet.Bullet(screen, ship)
            bullets.add(new)
    if j1.get_button(6) == 1:
        wasdown = True
    
    if j1.get_button(0) == 1 and j1.get_button(1) == 1:
        return "Quit"
    elif j2.get_button(0) == 1 and j2.get_button(1) == 1:
        return "Quit"
    else:
        return ""

def update_enemies(enemymap, pos, enemies, screen, ship):
    #print(len(enemymap), pos)
    won = False
    try:
        for i in range(0, len(enemymap)):
            #print(enemymap[i])
            if enemymap[i][pos] != 0:
                if enemymap[i][pos] == 1:
                    new = xanaliens.GreenAlien1(screen)
                elif enemymap[i][pos] == 2:
                    new = xanaliens.RedAlien1(screen)
                elif enemymap[i][pos] == 3:
                    new = xanaliens.BlueAlien1(screen, ship)
                elif enemymap[i][pos] == 4:
                    new = xanaliens.GreenAlien2(screen)
                elif enemymap[i][pos] == 5:
                    new = xanaliens.RedAlien2(screen)
                elif enemymap[i][pos] == 10:
                    new = xanaliens.BossAlien1(screen, ship)
                rect = screen.get_rect()
                new.y = (rect.height - 50) / len(enemymap) * i
                new.x = rect.right-134
                new.update()
                enemies.add(new)
    except IndexError:
        if len(enemies) == 0:
            won = True
    return enemies, won

def update_bullets(bullets, aliens, screen_rect):
    score = 0
    for bullet in bullets.copy():
        if bullet.rect.right >= screen_rect.right:
            #print("deleted")
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collisions:
        #print(collisions, type(collisions))
        for k, v in collisions.items():
            for i in v:
                if i.boss == False:
                    score += i.points
                    aliens.remove(i)
                else:
                    dead = i.hit()
                    if dead:
                        score += i.points
                        aliens.remove(i)
        #print(collisions)
    return score

class level1():
    def __init__(self, screen, levelpath="levels/1", levelnum=1, highscore=0, joystick=False):
        self.levelpath = levelpath
        self.joystick = joystick
        if self.joystick:
            self.joy1 = pygame.joystick.Joystick(0)
            self.joy1.init()
            self.joy2 = pygame.joystick.Joystick(1)
            self.joy2.init()
            print("got joysticks in level")
            pygame.mouse.set_visible(False)
        self.screen = screen
        self.player = xanplayer.Ship(screen)
        self.speed = 1
        self.lives = 3
        self.highscore = int(highscore)
        self.levelnum = levelnum
        self.quit = False
        self.lost = False
        self.goodshots = Group()
        self.badshots = Group()
        self.enemies = Group()
        self.screen_rect = self.screen.get_rect()
        #print("top", self.screen_rect.top)
        self.bg = pygame.image.load("xanfiles/space1.gif")
        self.lifeimg = pygame.image.load("xanfiles/playershipsmall.png")
        self.music = pygame.mixer.Sound("xanfiles/SpaceFlight.wav")
        with open(levelpath+"/enemies.txt") as obj:
            self.enemymap = json.load(obj)
        self.enemycounter = 0
        self.enemypos = 0
        self.won = False
        self.blue = pygame.color.Color("#00bcff")
        self.dblue= pygame.color.Color("#0000ff")
        self.black = pygame.color.Color("#000000")
        self.score = 0
    
    def init(self):
        #self.bg_color = (230, 230, 230)
        #self.screen.fill(self.bg_color)
        self.pic_rect = self.bg.get_rect()
        self.liferect = self.lifeimg.get_rect()
        self.liferect.top = self.screen_rect.top
        self.screen.blit(self.bg, self.pic_rect)
        font=pygame.font.Font('xanfiles/ARDESTINE.ttf', 50)
        words=font.render('Xandaar', True, self.blue)
        ywr=words.get_rect()
        ywr.bottom=self.screen_rect.bottom
        self.screen.blit(words, ywr)        
        pygame.display.flip()
        self.music.play(-1)
        #self.init_menu()
    
    def init_menu(self):
        nada = lambda: print("asdfad", sep=" ")
        #self.menu=pygameMenu.Menu(self.screen, 1000, 600, "xanfiles/ARDESTINE.ttf", "Game Paused", None, dopause=True)
        #self.menu.add_option('Exit', PYGAME_MENU_CLOSE)
        #self.menu.disable()
        
    
    def drawbar(self):
        pygame.draw.rect(self.screen, self.black, [self.screen_rect.right-200, self.screen_rect.bottom-50, 200, 50])
        font=pygame.font.Font('xanfiles/ARDESTINE.ttf', 20)
        score = font.render("Score: "+"{:,}".format(self.score), False, self.blue, self.black)
        ywr = score.get_rect()
        ywr.bottom = self.screen_rect.bottom - 25
        ywr.right=self.screen_rect.right
        self.screen.blit(score, ywr)
        
        hscore = font.render("High Score: "+"{:,}".format(self.highscore), False, self.blue, self.black)
        ywr = hscore.get_rect()
        ywr.bottom = self.screen_rect.bottom
        ywr.right=self.screen_rect.right
        self.screen.blit(hscore, ywr)        
        
        level = font.render("Level: "+str(self.levelnum), True, self.blue, self.black)
        ywr = level.get_rect()
        ywr.bottom = self.screen_rect.bottom
        ywr.centerx=self.screen_rect.centerx
        self.screen.blit(level, ywr)        
        
        pygame.display.flip()
    
    def pauseloop(self):
        done = False
        pos = list(self.screen_rect.center)
        pos.extend([50,100])
        mpos = (0,0)
        while not done:
            pygame.draw.rect(self.screen, self.dblue, pos)
                       
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mpos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    done = True
                    self.quit=True
            
            if pos[0] <= mpos[0] <= pos[0] + pos[2] and pos[1] <= mpos[1] <= pos[1] + pos[3]:
                done=True             
            
            pygame.display.flip()
        
    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit = True
                #print("quit")
            if self.joystick == False:
                if event.type == pygame.KEYDOWN:
                    checkkeydown(event, self.player, self.goodshots, self.screen)
                
                elif event.type == pygame.KEYUP:
                    checkkeyup(event, self.player, self.pauseloop)
            #else:
            #    checkjoyevents()
        if self.joystick:
            event=""
            do = checkjoystickevents(event, self.player, self.goodshots, self.screen, self.joy1, self.joy2)
            if do == "Quit":
                self.quit=True
        #self.menu.mainloop(events)
        if self.enemycounter >= 100:
            #print("updating enemies")
            self.enemycounter = 0
            self.enemypos += 1
            self.update_enemies()
        else:
            #print(self.enemycounter)
            self.enemycounter += 1
        if self.lives == 0:
            self.lost = True
        if self.score > self.highscore:
            self.highscore = self.score
        #self.menu.mainloop(events)
        
    def draw(self):
        self.drawbar()
        self.player.update()
        self.enemies.update()
        self.goodshots.update()
        self.badshots.update()
        
        self.score += update_bullets(self.goodshots, self.enemies, self.screen_rect)
        
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.lives -= 1
            #self.enemies.empty()
            for alien in self.enemies:
                if alien.rect.x <= 100:
                    alien.kill()
            self.badshots.empty()
            time.sleep(0.5)
        
        if pygame.sprite.spritecollideany(self.player, self.badshots):
            self.lives -= 1
            #self.enemies.empty()
            self.badshots.empty()
            time.sleep(0.5)
        
        #print(len(self.goodshots))
        #self.screen.fill(self.bg_color)
        self.screen.blit(self.bg, self.pic_rect)
        
        for i in range(self.lives):
            #print("making lives at", 0 + (20*i), 0)
            self.screen.blit(self.lifeimg, ((20*i), 0))
        
        self.player.blitme()
        for i in self.enemies:
            i.blitme()
            try:
                #if True:
                for b in i.fire():
                    self.badshots.add(b)
            except:
                #else:
                pass
        for bullet in self.goodshots.sprites():
            bullet.draw_bullet()
        for bullet in self.badshots.sprites():
            bullet.draw_bullet()
        pygame.display.flip()
    
    def end(self):
        font=pygame.font.Font('xanfiles/ARDESTINE.ttf', 20)
        level = font.render("Level "+str(self.levelnum)+" Completed!", False, self.blue, self.black)
        ywr = level.get_rect()
        ywr.center = self.screen_rect.center
        self.screen.blit(level, ywr)        
        
        pygame.display.flip()        
        pygame.mixer.stop()
        time.sleep(3)
    
    def update_enemies(self):
        self.enemies, self.won = update_enemies(self.enemymap, self.enemypos, self.enemies, self.screen, self.player)

if __name__ == "__main__":
    import Xandaar
    Xandaar.run_game()