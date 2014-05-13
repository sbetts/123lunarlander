## Lunar Lander Multiplayer Server
## Scott Betts; 76651961


import pygame, sys, random

from pygame.locals import *
from network import Listener, Handler, poll


pygame.init()
fpsClock = pygame.time.Clock()




windowSurfaceObj = pygame.display.set_mode((640,480))
pygame.display.set_caption('Lunar Lander')
landerSurfaceObj = pygame.image.load('lander.png')
blackColor = pygame.Color(0, 0, 0)
greyColor = pygame.Color(215, 215, 215)
gameWinLoseText = pygame.Surface((0, 0))
gameFont = pygame.font.Font(None, 18)



GRAVITY_CONSTANT = 0.0004
STARTING_LANDER_FUEL = 225


handlerList = {}
playerIDCounter = 1
landerList = {}
particleList = []


groundPoints = [(0, 400), (50, 400), (50, 450), (115, 450), (115, 350), (250, 350), (250, 410), (260, 410),
                (260, 450), (330, 450), (330, 320), (345, 320), (345, 375), (500, 375), (500, 360), (600, 360),
                (600, 460), (640, 460)]


groundRectList = [pygame.Rect(0, 400, 50, 80), pygame.Rect(50, 450, 65, 30), pygame.Rect(115, 350, 135, 130),
                  pygame.Rect(250, 410, 10, 70), pygame.Rect(260, 450, 70, 30), pygame.Rect(330, 320, 15, 160),
                  pygame.Rect(345, 375, 155, 105), pygame.Rect(500, 360, 100, 120), pygame.Rect(600, 460, 40, 20)]



tooFarRightMessage = 'You lose: lander left the playing field.'
tooFarLeftMessage = 'You lose: lander left the playing field.'
tooFastMessage = 'You lose: lander traveling too fast.'
tooSkewedMessage = 'You lose: lander crashed at an angle.'
unevenTerrainMessage = 'You lose: landing point too small.'
landersCollidedMessage = 'You lose: lander collided with another lander!'





class MyHandler(Handler):
     
    def on_open(self):
        global playerIDCounter
        handlerList[playerIDCounter] = self
        playerIDCounter += 1
        ##landerList[self] = Lander(generateStartingPosX(), generateStartingPosY(), 0, 0, 0, STARTING_LANDER_FUEL)
        landerList[self] = Lander(320, 80, 0, 0, 0, STARTING_LANDER_FUEL)
        pass
         
    def on_close(self):
        ##del landerList[self]
        pass
     
    def on_msg(self, msg):
        if msg.has_key('command'):
            landerList[self].setCommand(msg['command'])


class Lander:


    def __init__(self, startingPosX, startingPosY, startingVelocityX, startingVelocityY, startingAngle, startingFuel):
        self._posX = startingPosX
        self._posY = startingPosY
        self._velocityX = startingVelocityX
        self._velocityY = startingVelocityY
        self._angle = startingAngle
        self._fuel = startingFuel
        self._xAcceleration = 0
        self._yAcceleration = 0
        self._landerRect = windowSurfaceObj.blit(landerSurfaceObj, (self._posX, self._posY))
        self._shouldMove = True
        self._hasWon = False
        self._command = 0


    def getPosX(self):
        return self._posX


    def getPosY(self):
        return self._posY


    def getVelocityX(self):
        return self._velocityX


    def getVelocityY(self):
        return self._velocityY


    def getPlayerID(self):
        return self._playerID


    def getAngle(self):
        return self._angle


    def getFuel(self):
        return self._fuel


    def getRect(self):
        return self._landerRect


    def setMoving(self, shouldMove):
        self._shouldMove = shouldMove


    def getHasWon(self):
        return self._hasWon


    def setWon(self, hasWon):
        self._hasWon = hasWon


    def setCommand(self, command):
        self._command = command


    def update(self):
        if self._shouldMove == True:
            if self._command == 1:
                if self._angle >= 0 and self._angle <= 90 and self._fuel > 0:
                    xValue = self._angle / 90.0
                    self._velocityY -= (1 - xValue) * 0.15
                    self._velocityX += 0.3 * -xValue
                    self._yAcceleration = 0
                    self._fuel = self._fuel - 1
                    for x in range(3):
                        particleList.append(PropulsionParticle(self._posX, self._posY, self._velocityX, self._velocityY))
                if self._angle < 0 and self._angle >= -90 and self._fuel > 0:
                    xValue = self._angle / 90.0
                    self._velocityY -= (1 - -xValue) * 0.15
                    self._velocityX += 0.3 * -xValue
                    self._yAcceleration = 0
                    self._fuel = self._fuel - 1
                    for x in range(3):
                        particleList.append(PropulsionParticle(self._posX, self._posY, self._velocityX, self._velocityY))
                self._command = 0
            if self._command == 2:
                self._angle += 5
                if self._angle > 90:
                    self._angle = 90
                self._command = 0
            if self._command == 3:
                self._angle -= 5
                if self._angle < -90:
                    self._angle = -90
                self._command = 0
            self._yAcceleration += GRAVITY_CONSTANT
            self._velocityY += self._yAcceleration
            self._posY += self._velocityY
            self._posX += self._velocityX
        self._landerRect = windowSurfaceObj.blit(pygame.transform.rotate(landerSurfaceObj, self._angle), (self._posX, self._posY))



class PropulsionParticle:


    def __init__(self, startingPosX, startingPosY, startingVelocityX, startingVelocityY):
        self._posX = startingPosX + 10
        self._posY = startingPosY + 30
        self._velocityX = -startingVelocityX * 4 * random.random() + random.random() - random.random()
        self._velocityY = -startingVelocityY + 3
        self._lifetime = 30 + (30 * random.random())
        self._isAlive = True


    def update(self):
        if self._lifetime <= 0:
            self._isAlive = False
        self._posX = self._posX + self._velocityX
        self._posY = self._posY + self._velocityY
        self._lifetime = self._lifetime - 1


    def queuedForRemoval(self):
        return not self._isAlive


    def getPosX(self):
        return self._posX

    def getPosY(self):
        return self._posY


def checkForCollision(lander1, lander2):
    if lander1.getRect().colliderect(lander2.getRect()) == True:
        playerLoses(lander1, landersCollidedMessage)
        playerLoses(lander2, landersCollidedMessage)
        return True



def checkForLanding(lander, landerLoc):
    if lander.getRect().centerx > 640:
        playerLoses(lander, tooFarRightMessage)
        return True
    elif lander.getRect().right < 5:
        playerLoses(lander, tooFarLeftMessage)
        return True
    elif lander.getRect().collidelist(groundRectList) != -1:
        if lander.getVelocityY >= 1:
            playerLoses(lander, tooFastMessage)
            return True
        elif lander.getAngle() > 5:
            playerLoses(lander, tooSkewedMessage)
            return True
        elif lander.getAngle() < -5:
            playerLoses(lander, tooSkewedMessage)
            return True
        else:
            if groundRectList[lander.getRect().collidelist(groundRectList)].collidepoint(lander.getRect().bottomleft):
                if groundRectList[lander.getRect().collidelist(groundRectList)].collidepoint(lander.getRect().bottomright):
                    ##PLAYER WINS HERE
                    lander.setMoving(False)
                    lander.hasWon(True)
                else:
                    playerLoses(lander, unevenTerrainMessage)
                    return True
            else:
                playerLoses(lander, unevenTerrainMessage)
                return True


def playerLoses(lander, lossMessage):
    if lander.getHasWon() == False:
        pass
        ##PLAYER GAME OVER GOES HERE


def destroyLander(landerLoc):
    ##LANDER EXPLOSION CODE GOES HERE
    del landerList[landerLoc]
    print('Successfully destroyed lander.')
    if len(landerList) == 0:
        pass
        ##SERVER GAME OVER GOES HERE



def generateGameStateForClients(thisLanderList, thisParticleList):
    landerListForClients = []
    particleListForClients = []
    gameState = {}
    for x in thisLanderList:
        landerListForClients.append([thisLanderList[x].getAngle(), thisLanderList[x].getPosX(), thisLanderList[x].getPosY()])
    gameState['landerList'] = landerListForClients
    for x in thisParticleList:
        particleListForClients.append([x.getPosX(), x.getPosY()])
    gameState['particleList'] = particleListForClients
    return gameState


def sendGameStateToClients(gameState):
    for x in handlerList:
        handlerList[x].do_send(gameState)

port = 8888
server = Listener(port, MyHandler)

while True:
    windowSurfaceObj.fill(blackColor)


    pygame.draw.lines(windowSurfaceObj, greyColor, False, groundPoints)

    poll(timeout=0.05)

    for x in particleList:
        pygame.draw.rect(windowSurfaceObj, greyColor, pygame.Rect(x.getPosX(), x.getPosY(), 2, 2))


    




    
    for x in landerList:
        landerList[x].update()
    for x in particleList:
        x.update()
        if x.queuedForRemoval():
            particleList.remove(x)
    landersToBeDestroyed = set()
    for x in landerList:
        for y in landerList:
            if landerList[x] != landerList[y]:
                if checkForCollision(landerList[x], landerList[y]):
                    landersToBeDestroyed.add(x)
                    landersToBeDestroyed.add(y)
    for x in landerList:
        if checkForLanding(landerList[x], x):
            landersToBeDestroyed.add(x)
    for x in landersToBeDestroyed:
        destroyLander(x)
    currentGameStateForClients = generateGameStateForClients(landerList, particleList)
    sendGameStateToClients(currentGameStateForClients)
    
    pygame.display.update()
    fpsClock.tick(30)
