## Lunar Lander Multiplayer Client
## Scott Betts; 76651961



import pygame, sys, random
from network import Handler, poll
from threading import Thread
from time import sleep

from pygame.locals import *


pygame.init()
fpsClock = pygame.time.Clock()




windowSurfaceObj = pygame.display.set_mode((640,480))
pygame.display.set_caption('Lunar Lander')
landerSurfaceObj = pygame.image.load('playerlander2.png')
blackColor = pygame.Color(0, 0, 0)
greyColor = pygame.Color(215, 215, 215)
gameWinLoseText = pygame.Surface((0, 0))
gameStartScreenText = pygame.Surface((0, 0))
startFont = pygame.font.Font(None, 26)
startFont2 = pygame.font.Font(None, 22)
gameMenuText1 = pygame.Surface((0, 0))
gameMenuText2 = pygame.Surface((0, 0))
gameMenuText3 = pygame.Surface((0, 0))
gameSelectorText1 = pygame.Surface((0, 0))
gameSelectorText2 = pygame.Surface((0, 0))
gameInstructionText1 = pygame.Surface((0, 0))
gameInstructionText2 = pygame.Surface((0, 0))
gameFont = pygame.font.Font(None, 18)
landerYVelocityText = pygame.Surface((0, 0))
landerPlayerIdentifierText = pygame.Surface((0, 0))




landerList = []
particleList = []


keyIsDown = False
gameOver = False
should_exit = False
downKey = 0

pygame.key.set_repeat(33, 33)



groundPoints = [(0, 400), (50, 400), (50, 450), (115, 450), (115, 350), (250, 350), (250, 410), (260, 410),
                (260, 450), (330, 450), (330, 320), (345, 320), (345, 375), (500, 375), (500, 360), (600, 360),
                (600, 460), (640, 460)]



groundRectList = [pygame.Rect(0, 400, 50, 80), pygame.Rect(50, 450, 65, 30), pygame.Rect(115, 350, 135, 130),
                  pygame.Rect(250, 410, 10, 70), pygame.Rect(260, 450, 70, 30), pygame.Rect(330, 320, 15, 160),
                  pygame.Rect(345, 375, 155, 105), pygame.Rect(500, 360, 100, 120), pygame.Rect(600, 460, 40, 20)]



class Client(Handler):
    
    def on_close(self):
        global should_exit
        should_exit = True
        
    def on_msg(self, msg):
        if msg.has_key('playerid'):
            self._playerID = msg['playerid']
        else:
            global landerList
            global particleList
            landerList = msg['landerList']
            particleList = msg['particleList']


    def getPlayerID(self):
        return self._playerID



def checkForKeyPress():
    downKey = 0
    if pygame.event.peek(KEYDOWN) == False:
        keyIsDown = False

    for event in pygame.event.get():
        downKey = 0
        if gameOver == True:
            pygame.quit()
            sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            keyIsDown = True
            if event.key == K_UP:
                downKey = 1 # 1 is up arrow.
            elif event.key == K_LEFT:
                downKey = 2 # 2 is left arrow.
            elif event.key == K_RIGHT:
                downKey = 3 # 3 is right arrow.
            elif event.key == K_ESCAPE:
                downKey = 4 # 4 is a dummy value.
                pygame.event.post(pygame.event.Event(QUIT))

    return downKey


        
def checkForMenuKeyPress():
    downKey = 0
    if pygame.event.peek(KEYDOWN) == False:
        keyIsDown = False

    for event in pygame.event.get():
        downKey = 0
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            keyIsDown = True
            if event.key == K_UP:
                downKey = 1 # 1 is up arrow.
            elif event.key == K_DOWN:
                downKey = 2 # 2 is down arrow.
            elif event.key == K_RETURN:
                downKey = 3 # 3 is return.
            elif event.key == K_ESCAPE:
                downKey = 4 # 4 is a dummy value.
                pygame.event.post(pygame.event.Event(QUIT))

    return downKey



def sendCommandToServer(client, command):
    client.do_send({'command': command})



def beginGame():

    host, port = '169.234.87.121', 8888
    client = Client(host, port)

    has_lander = False
    game_over = False

    game_over_tick = 0


    while game_over_tick < 120:

        if game_over == True:
            game_over_tick += 1
            
        if should_exit == True:
            ##print('**** Disconnected from server ****')
            ##sys.exit()
            pass

        poll()
        
        windowSurfaceObj.fill(blackColor)


        pygame.draw.lines(windowSurfaceObj, greyColor, False, groundPoints)
        
        for x in particleList:
            pygame.draw.rect(windowSurfaceObj, greyColor, pygame.Rect(x[0], x[1], 2, 2))

        
        for x in landerList:
            if x[7] != 'DESTROYED':
                windowSurfaceObj.blit(pygame.transform.rotate(landerSurfaceObj, x[0]), (x[1], x[2]))

        for x in landerList:
            try:
                if x[4] == client.getPlayerID():
                    has_lander = True
                    myLander = x
            except:
                pass

        if has_lander:
                if myLander[5] != '':
                    game_over = True
                    gameWinLoseText = gameFont.render(myLander[5], True, greyColor)

        if has_lander:
            landerPlayerIdentifierText = gameFont.render('You', True, greyColor)
            windowSurfaceObj.blit(landerPlayerIdentifierText, (myLander[1], myLander[2] - 20))
            landerFuelText = gameFont.render('Lander Y Velocity: ' + str(myLander[6]), True, greyColor)
            windowSurfaceObj.blit(landerFuelText, (400, 30))

        if game_over:
            windowSurfaceObj.blit(gameWinLoseText, (30, 30))

        if has_lander:
            landerFuelText = gameFont.render('Lander Fuel: ' + str(myLander[3]), True, greyColor)
            windowSurfaceObj.blit(landerFuelText, (400, 50))

        userCommand = checkForKeyPress()

        sendCommandToServer(client, userCommand)

        
        pygame.display.update()
        fpsClock.tick(30)

    client.do_close()



def startScreen():
    exit_game = False
    player_selection = 1
    while exit_game == False:
        windowSurfaceObj.fill(blackColor)
        gameStartScreenText = startFont.render('LUNAR LANDER', True, greyColor)
        windowSurfaceObj.blit(gameStartScreenText, (150, 115))
        windowSurfaceObj.blit(landerSurfaceObj, (100, 115))
        gameMenuText1 = startFont2.render('MAIN MENU', True, greyColor)
        windowSurfaceObj.blit(gameMenuText1, (150, 145))
        gameMenuText2 = gameFont.render('START GAME', True, greyColor)
        windowSurfaceObj.blit(gameMenuText2, (150, 175))
        gameMenuText3 = gameFont.render('EXIT', True, greyColor)
        windowSurfaceObj.blit(gameMenuText3, (150, 190))
        gameInstructionText1 = gameFont.render('Up arrow key to fire thrusters, left and right arrow keys to rotate.', True, greyColor)
        gameInstructionText2 = gameFont.render('Land flat on the moon, but make it a soft landing!', True, greyColor)
        windowSurfaceObj.blit(gameInstructionText1, (200, 270))
        windowSurfaceObj.blit(gameInstructionText2, (200, 290))
        if player_selection == 1:
            gameSelectorText1 = gameFont.render('>>>', True, greyColor)
            windowSurfaceObj.blit(gameSelectorText1, (110, 173))
            gameSelectorText2 = gameFont.render('<<<', True, greyColor)
            windowSurfaceObj.blit(gameSelectorText2, (250, 173))
        elif player_selection == 2:
            gameSelectorText1 = gameFont.render('>>>', True, greyColor)
            windowSurfaceObj.blit(gameSelectorText1, (110, 188))
            gameSelectorText2 = gameFont.render('<<<', True, greyColor)
            windowSurfaceObj.blit(gameSelectorText2, (250, 188))

        userMenuCommand = checkForMenuKeyPress()

        if userMenuCommand == 1 or userMenuCommand == 2:
            if player_selection == 1:
                player_selection = 2
            else:
                player_selection = 1
        if userMenuCommand == 3:
            if player_selection == 1:
                beginGame()
            else:
                pygame.quit()
                sys.exit()
            
        pygame.display.update()
        fpsClock.tick(30)
            
startScreen()


