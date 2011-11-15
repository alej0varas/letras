#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys
import pygame
from pygame.locals import *
import random
#import time

# Constantes
#WIDTH = 640
WIDTH = 1280
#HEIGHT = 480
HEIGHT = 740

AGE_FACTOR = 1
DEAD_AGE = 150
TAMANO_INICIAL = 10

# Clases
# ---------------------------------------------------------------------
class Letra(pygame.sprite.Sprite):
    def __init__(self, texto, group):
        super(Letra, self).__init__(group)
        self.texto = texto
        self._image, self._rect = texto_to_img(texto, TAMANO_INICIAL, 0, 0)
        self.posx = random.randint(0, WIDTH - self._rect.width)
        self.posy = random.randint(0, HEIGHT -self._rect.height)
        self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        self.age = TAMANO_INICIAL

    def update(self):
        _change = None
        self.age += AGE_FACTOR
        tamano = self.age
        if not self.age % 10:
            self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
#            print self.color
        self.image, self.rect = texto_to_img(self.texto, tamano, self.posx, self.posy, self.color) 

        # don't disapear in borders
        # x
        if self.posx + self.rect.width/2 > WIDTH:
            self.posx -= AGE_FACTOR
            _change = True
        if self.posx - self.rect.width/2 < 0:
            self.posx += AGE_FACTOR
            _change = True
        # y
        if self.posy + self.rect.height/2 > HEIGHT:
            self.posy -= AGE_FACTOR
            _change = True
        if self.posy - self.rect.height/2 < 0:
            self.posy += AGE_FACTOR
            _change = True
        if _change:
            self.image, self.rect = texto_to_img(self.texto, tamano, self.posx, self.posy, self.color)

        if self.age > DEAD_AGE:
            self.kill()
        
class Letras(pygame.sprite.Group):
    def __init__(self, **kwargs):
        super(Letras, self).__init__(**kwargs)

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------
def texto_to_img(texto, tamano, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("images/DroidSans.ttf", tamano)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

def clear_callback(surf, rect):
        surf.blit(surf, rect, rect)

# ---------------------------------------------------------------------

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Letras")
    print 'images/fondo%dx%d.png' % (WIDTH, HEIGHT)
    background_image = pygame.image.load('images/fondo%dx%d.png' % (WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    letras = Letras()

    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        event = pygame.event.get(2)
        pygame.event.clear()
        if len(event):
            event = event.pop()
            if event.type == 2 and event.dict['key'] == K_ESCAPE:
                sys.exit(0)
            if event.type == 2:
                if 33 < event.dict['key'] and event.dict['key'] < 126:
                    letra = Letra(event.dict['unicode'], letras)
        letras.update()
        letras.clear(screen, clear_callback)
        letras.draw(screen)
        pygame.display.flip()
        screen.blit(background_image, (0, 0))


if __name__ == '__main__':
    pygame.init()
    main()
