## Lunar Lander Clone
## Scott Betts; 76651961


import pygame, sys, random
from pygame.locals import *


pygame.init()
fpsClock = pygame.time.Clock()


windowSurfaceObj = pygame.display.set_mode((640,480))
pygame.display.set_caption('Lunar Lander')
landerSurfaceObj = pygame.image.load('lander.png')
blackColor = pygame.Color(0, 0, 0)
greyColor = pygame.Color(215, 215, 215)
gameWinLoseText = pygame.Surface((0, 0))
landerYVelocityText = pygame.Surface((0, 0))
landerFuelText = pygame.Surface((0, 0))
gameFont = pygame.font.Font(None, 18)


landerPosX = 320
landerPosY = 80

landerFuel = 400
landerXVelocity = 0
landerYVelocity = 0.1
landerXAcceleration = 0
landerYAcceleration = 0
landerAngle = 0
keyIsDown = False
gameOver = False

pygame.key.set_repeat(33, 33)

GRAVITY_CONSTANT = 0.0004

particleList = []

groundPoints = [(0, 400), (50, 400), (50, 450), (115, 450), (115, 350), (250, 350), (250, 410), (260, 410), (260, 450), (330, 450), (330, 320), (345, 320), (345, 375), (500, 375), (500, 360), (600, 360), (600, 460), (640, 460)]
groundRectList = [pygame.Rect(0, 400, 50, 80), pygame.Rect(50, 450, 65, 30), pygame.Rect(115, 350, 135, 130), pygame.Rect(250, 410, 10, 70), pygame.Rect(260, 450, 70, 30), pygame.Rect(330, 320, 15, 160), pygame.Rect(345, 375, 155, 105), pygame.Rect(500, 360, 100, 120), pygame.Rect(600, 460, 40, 20)]

class PropulsionParticle:


    def __init__(self, startingPosX, startingPosY, startingVelocityX, startingVelocityY):
        self._posX = startingPosX + 10
        self._posY = startingPosY + 30
        self._velocityX = -startingVelocityX * 2 * random.random()
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


while True:
    windowSurfaceObj.fill(blackColor)


    pygame.draw.lines(windowSurfaceObj, greyColor, False, groundPoints)
    
    for x in particleList:
        pygame.draw.rect(windowSurfaceObj, greyColor, pygame.Rect(x.getPosX(), x.getPosY(), 2, 2))


    landerRect = windowSurfaceObj.blit(landerSurfaceObj, (landerPosX, landerPosY))

    if gameOver == True:
        windowSurfaceObj.blit(gameWinLoseText, (30, 30))

    if landerYVelocity > 1:
        landerYVelocityText = gameFont.render('Lander Y Velocity: ' + str(-landerYVelocity), True, (255, 0, 0))
    else:
        landerYVelocityText = gameFont.render('Lander Y Velocity: ' + str(-landerYVelocity), True, greyColor)
    windowSurfaceObj.blit(landerYVelocityText, (400, 30))
    landerFuelText = gameFont.render('Lander Fuel: ' + str(landerFuel), True, greyColor)
    windowSurfaceObj.blit(landerFuelText, (400, 50))

    if pygame.event.peek(KEYDOWN) == False:
        keyIsDown = False

    for event in pygame.event.get():
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

    if keyIsDown == True:
        if downKey == 1:
            if landerAngle >= 0 and landerAngle <= 90 and landerFuel > 0:
                xValue = landerAngle / 90.0
                landerYVelocity -= (1 - xValue) * 0.15
                landerXVelocity += 0.3 * -xValue
                landerYAcceleration = 0
                landerFuel = landerFuel - 1
                particleList.append(PropulsionParticle(landerPosX, landerPosY, landerXVelocity, landerYVelocity))
            if landerAngle < 0 and landerAngle >= -90 and landerFuel > 0:
                xValue = landerAngle / 90.0
                landerYVelocity -= (1 - -xValue) * 0.15
                landerXVelocity += 0.3 * -xValue
                landerYAcceleration = 0
                landerFuel = landerFuel - 1
                particleList.append(PropulsionParticle(landerPosX, landerPosY, landerXVelocity, landerYVelocity))
        elif downKey == 2:
            landerAngle += 5
            if landerAngle > 90:
                landerAngle = 90
            landerSurfaceObj = pygame.image.load('lander.png')
            landerSurfaceObj = pygame.transform.rotate(landerSurfaceObj, landerAngle)
        elif downKey == 3:
            landerAngle -= 5
            if landerAngle < -90:
                landerAngle = -90
            landerSurfaceObj = pygame.image.load('lander.png')
            landerSurfaceObj = pygame.transform.rotate(landerSurfaceObj, landerAngle)


    for x in particleList:
        x.update()
        if x.queuedForRemoval():
            particleList.remove(x)

    landerYAcceleration += GRAVITY_CONSTANT
    landerYVelocity += landerYAcceleration
    landerPosY += landerYVelocity
    landerPosX += landerXVelocity


    if gameOver == False:
        if landerRect.centerx > 640:
            print('Too far right.')
            gameWinLoseText = gameFont.render('You lose: lander left the playing field.', True, greyColor)
            gameOver = True
            landerYVelocity = 0
            landerYAcceleration = 0
            landerXVelocity = 0
            GRAVITY_CONSTANT = 0
        if landerRect.right < 5:
            print('Too far left.')
            gameWinLoseText = gameFont.render('You lose: lander left the playing field.', True, greyColor)
            gameOver = True
            landerYVelocity = 0
            landerYAcceleration = 0
            landerXVelocity = 0
            GRAVITY_CONSTANT = 0
        if landerRect.collidelist(groundRectList) != -1:
            if landerYVelocity >= 1:
                print('Too fast.')
                gameWinLoseText = gameFont.render('You lose: lander traveling too fast.', True, greyColor)
                gameOver = True
            elif landerAngle > 5:
                print('Too skewed.')
                gameWinLoseText = gameFont.render('You lose: lander crashed at an angle.', True, greyColor)
                gameOver = True
            elif landerAngle < -5:
                print('Too skewed.')
                gameWinLoseText = gameFont.render('You lose: lander crashed at an angle.', True, greyColor)
                gameOver = True
            else:
                if groundRectList[landerRect.collidelist(groundRectList)].collidepoint(landerRect.bottomleft):
                    if groundRectList[landerRect.collidelist(groundRectList)].collidepoint(landerRect.bottomright):
                        print('You win!')
                        gameWinLoseText = gameFont.render('You Win!', True, greyColor)
                        gameOver = True
                    else:
                        print('Surface uneven.')
                        gameWinLoseText = gameFont.render('You lose: landing point too small.', True, greyColor)
                        gameOver = True
                else:
                    print('Surface uneven.')
                    gameWinLoseText = gameFont.render('You lose: landing point too small.', True, greyColor)
                    gameOver = True
            landerYVelocity = 0
            landerYAcceleration = 0
            landerXVelocity = 0
            GRAVITY_CONSTANT = 0

    pygame.display.update()
    fpsClock.tick(30)
