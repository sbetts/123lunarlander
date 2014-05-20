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
landerSurfaceObj = pygame.image.load('lander.png')
blackColor = pygame.Color(0, 0, 0)
greyColor = pygame.Color(215, 215, 215)
gameWinLoseText = pygame.Surface((0, 0))
gameFont = pygame.font.Font(None, 18)
landerYVelocityText = pygame.Surface((0, 0))




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


        

host, port = 'localhost', 8888
client = Client(host, port)


def sendCommandToServer(command):
    client.do_send({'command': command})


def periodic_poll():
    while 1:
        poll()
        sleep(0.05)


thread = Thread(target=periodic_poll)
thread.daemon = True
thread.start()

has_lander = False
game_over = False


while True:
    if should_exit == True:
        ##print('**** Disconnected from server ****')
        ##sys.exit()
        pass
    windowSurfaceObj.fill(blackColor)


    pygame.draw.lines(windowSurfaceObj, greyColor, False, groundPoints)
    
    for x in particleList:
        pygame.draw.rect(windowSurfaceObj, greyColor, pygame.Rect(x[0], x[1], 2, 2))

    
    for x in landerList:
        windowSurfaceObj.blit(pygame.transform.rotate(landerSurfaceObj, x[0]), (x[1], x[2]))

    for x in landerList:
        if x[4] == client.getPlayerID():
            has_lander = True
            myLander = x

    if has_lander:
            if myLander[5] != '':
                game_over = True
                gameWinLoseText = gameFont.render(myLander[5], True, greyColor)

    if has_lander:
        landerFuelText = gameFont.render('Lander Y Velocity: ' + str(myLander[6]), True, greyColor)
        windowSurfaceObj.blit(landerFuelText, (400, 30))

    if game_over:
        windowSurfaceObj.blit(gameWinLoseText, (30, 30))

    if has_lander:
        landerFuelText = gameFont.render('Lander Fuel: ' + str(myLander[3]), True, greyColor)
        windowSurfaceObj.blit(landerFuelText, (400, 50))

    userCommand = checkForKeyPress()

    sendCommandToServer(userCommand)

    
    pygame.display.update()
    fpsClock.tick(30)
