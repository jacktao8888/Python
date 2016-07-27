#当前目录下，创建/resources/，里面分别存放audio和images文件

import pygame
from pygame.locals import *

pygame.init()
width,height = 640,480
screen = pygame.display.set_mode((width, height))
keys = [False,False,False,False]
playerpos = [100,100]

player = pygame.image.load("resources/images/dude.png")

while 1:
    screen.fill(0)
    
    screen.blit(player, playerpos)
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys[0] = True
            elif event.key == pygame.K_s:
                keys[1] = True
            elif event.key == pygame.K_a:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_s:
                keys[1] = False
            elif event.key == pygame.K_a:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
    
    if keys[0]:
        playerpos[1] -= 5
    elif keys[1]:
        playerpos[1] += 5
    elif keys[2]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5
    
    if playerpos[0] > 576:
        playerpos[0] = 576
    elif playerpos[0] < 0:
        playerpos[0] = 0
    
    if playerpos[1] > 434:
        playerpos[1] = 434
    elif playerpos[1] < 0:
        playerpos[1] = 0
