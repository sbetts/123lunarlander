## whalebot.py
## Author: Scott Betts
## SID: 76651961
## Original Code: Thomas Debeauvais

from random import randint
from time import sleep
from common import *

################### CONTROLLER #############################

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT

class Controller():
    def __init__(self, m):
        self.m = m
        pygame.init()
    
    def poll(self):
        cmd = None
        our_rand = randint(0, 3)
        if our_rand == 0:
            cmd = 'up'
        elif our_rand == 1:
            cmd = 'down'
        elif our_rand == 2:
            cmd = 'left'
        elif our_rand == 3:
            cmd = 'right'
        if cmd:
            self.m.do_cmd(cmd)

################### VIEW #############################

class View():
    def __init__(self, m):
        self.frame_counter = 0
        self.m = m
        
    def display(self):
        self.frame_counter += 1
        if self.frame_counter >= 50:
            self.frame_counter = 0
            print("Position: " + str(self.m.mybox[0]) + ", " + str(self.m.mybox[1]))

################### LOOP #############################

model = Model()
c = Controller(model)
v = View(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()
