import pygame
from pygame import *
import socket

sizeX = 8
sizeY = 8

# socket init
HOST = 'table.apokalypse.email'
PORT = 1337
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def pixel(x, y, r, g, b, a=255):
    if a == 255:
        sock.send(b'PX %d %d %02x%02x%02x\n' % (x, y, r, g, b))
    else:
        sock.send(b'PX %d %d %02x%02x%02x%02x\n' % (x, y, r, g, b, a))


pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.key.set_repeat(20, 20)

running = True
offset = [0, 10]
while running:
    keys_pressed = pygame.event.get()  # pygame.event.get(pygame.KEYDOWN)
    for event in keys_pressed:
        if event.type == pygame.KEYDOWN:
            if event.key == K_s:
                offset[1] = offset[1] + 1
            if event.key == K_w:
                offset[1] = offset[1] - 1
        elif event.type == pygame.QUIT:
            running = False
    for x in range(sizeX + 1):
        for y in range(sizeY + 1):
            pixel(x + offset[0], y + offset[1], 0x00, 0xFF, 0xFF)
    pygame.time.wait(20)
