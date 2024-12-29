import pygame
from pygame import *
import socket
from random import randint, random

##### CONFIG #####
HOST = 'table.apokalypse.email'
PORT = 1337
GlobalOffset = [0, 800]
PadelGraceRange = 1
ClutchRadius = 5
ScoreboardOffset = 8

# socket init
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# pygame init
pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.key.set_repeat(20, 20)

# pixel definition
def pixel(x, y, r, g, b, a=255):
    if a == 255:
        sock.send(b'PX %d %d %02x%02x%02x\n' % (x, y, r, g, b))
    else:
        sock.send(b'PX %d %d %02x%02x%02x%02x\n' % (x, y, r, g, b, a))

# random ball speed
def ballSpedRand():
    tempX = randint(1, 2)
    if random() > 0.5:
        tempX = -tempX
    tempY = randint(1, 2)
    if random() > 0.5:
        tempY = -tempY
    return [tempX, tempY]

# var init
sizeX = 4
sizeY = 40
catch1 = 0
catch2 = 0
running = True
Player1Offset = [0, 12]
Player2Offset = [128, 12]
BallOffset = [64, 32]
BallSpeed = ballSpedRand()

while running:
    # key controls
    keys_pressed = pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        Player1Offset[1] -= 1
    if keys[K_s]:
        Player1Offset[1] += 1
    if keys[K_UP]:
        Player2Offset[1] -= 1
    if keys[K_DOWN]:
        Player2Offset[1] += 1

    # rendering
    # left pedal
    for x in range(sizeX + 1):
        for y in range(sizeY + 1):
            pixel(x + Player1Offset[0] + GlobalOffset[0], y + Player1Offset[1] + GlobalOffset[1], 0xFF, 0xFF, 0xFF)
    # right pedal
    for x in range(sizeX + 1):
        for y in range(sizeY + 1):
            pixel(x + Player2Offset[0] + GlobalOffset[0], y + Player2Offset[1] + GlobalOffset[1], 0xFF, 0xFF, 0xFF)
    # ball
    for x in range(5):
        for y in range(5):
            pixel(x + BallOffset[0] + GlobalOffset[0], y + BallOffset[1] + GlobalOffset[1], 0xFF, 0xFF, 0xFF)
    # bottom reminder
    for x in range(17):
        for y in range(3):
            pixel(x + 64 + GlobalOffset[0], y + 64 + GlobalOffset[1], 0xFF, 0xFF, 0xFF)
    # score render left
    for x in range(9 - 2 * catch1):
        for y in range(3):
            pixel(x + 2 * catch1 + GlobalOffset[0] + 64 - ScoreboardOffset, y + GlobalOffset[1], 0xFF, 0xFF, 0xFF)
    # score render right
    for x in range(9 - 2 * catch2):
        for y in range(3):
            pixel(x + GlobalOffset[0] + 64 + ScoreboardOffset, y + GlobalOffset[1], 0xFF, 0xFF, 0xFF)

    # ball movement
    BallOffset[0] += BallSpeed[0]
    BallOffset[1] += BallSpeed[1]

    # collision detection
    # left pedal
    if BallOffset[0] <= Player1Offset[0] + sizeX / 2 and BallOffset[1] > Player1Offset[1] - PadelGraceRange and BallOffset[1] < Player1Offset[1] + sizeY + PadelGraceRange:
        BallSpeed[0] = -BallSpeed[0]
    # right pedal
    if BallOffset[0] >= Player2Offset[0] - sizeX / 2 and BallOffset[1] > Player2Offset[1] - PadelGraceRange and BallOffset[1] < Player2Offset[1] + sizeY + PadelGraceRange:
        BallSpeed[0] = -BallSpeed[0]
    # oben unten
    if BallOffset[1] + GlobalOffset[1] > GlobalOffset[1] + 64 or BallOffset[1] + GlobalOffset[1] < GlobalOffset[1]:
        BallSpeed[1] =- BallSpeed[1]

    # goal detection
    # left
    if BallOffset[0] <= Player1Offset[0] - ClutchRadius:
        BallOffset = [64, 32]
        BallSpeed = ballSpedRand()
        catch1 += 1
    # right
    if BallOffset[0] >= Player2Offset[0] + ClutchRadius:
        BallOffset = [64, 32]
        BallSpeed = ballSpedRand()
        catch2 += 1

    # game over
    if catch1 == 4 or catch2 == 4:
        print("Catch1: " + str(catch1) + ", Catch2: " + str(catch2))
        for i in range(21):
            for x in range(129):
                for y in range(65):
                    pixel(x + GlobalOffset[0], y + GlobalOffset[1], 0xFF, 0xFF, 0xFF)
            pygame.time.wait(20)
        catch1 = 0
        catch2 = 0

    # fps
    pygame.time.wait(20)
