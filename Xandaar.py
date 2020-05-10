import sys, os, time
import pygame
import xanlevel

 
def run_game():
    global xanlevel
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() >= 2:
        joystick = True
    else:
        joystick = False
    print("Joystick", joystick)
    screen = pygame.display.set_mode((1000, 650))
    pygame.display.set_caption("Xandaar")
    
    levels = [xanlevel.level1]
    levelspaths = []
    
    for path, folder, file in os.walk("xanlevels"):
        if folder != [] and type(folder) == list:
            levelspaths.extend(folder)
    
    levelspaths = sorted(levelspaths)
    print(levelspaths)
    
    levelnum = 0
    #level = levels[levelnum](screen)
    
    with open("xanfiles/highscore.txt") as obj:
        highscore = obj.read()
    
    highscoreorg = int(highscore)
    
    lost = False
    quit = False
    won = False
    score = 0
    while won != True or lost != True or quit != True:
        #if quit != True:
        #if True:
        print(levelnum)
        levelcurrent = xanlevel.level1(screen, "xanlevels/"+levelspaths[levelnum], levelnum+1, highscore, joystick)
        levelcurrent.init()
        levelcurrent.score = score
        while won != True or lost != True or quit != True:
            levelcurrent.events()
            levelcurrent.draw()
            
            if levelcurrent.quit == True:
                pygame.quit()
                quit = True
                sys.exit()
            if levelcurrent.won == True:
                score = levelcurrent.score
                highscore = levelcurrent.highscore
                levelcurrent.end()
                #print("level won")
                break
            if levelcurrent.lost == True:
                score = levelcurrent.score
                highscore = levelcurrent.highscore
                lost = True
                break
        #print("level ended")
        if highscore > highscoreorg:
            with open("xanfiles/highscore.txt", "w") as obj:
                obj.write(str(highscore))
        if quit == False:
            print("added 1 to", levelnum, "\nnew level")
            levelnum += 1
        if levelnum == len(levelspaths):
            print("levelnum", levelnum)
            print("won")
            won = True
            break
        if lost == True:
            print("lost the game")
            break

if __name__ == "__main__":
    run_game()
    pygame.quit()