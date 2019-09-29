#! /usr/bin/env python

"""
This script implements a basic sprite that can move in all 8 directions.

-Written by Sean J. McKiernan 'Mekire'
"""

import os
import sys

import pygame as pg


CAPTION = "Mova com ASDW, pule com Espaço"
SCREEN_SIZE = (500, 500)

TRANSPARENT = (0, 0, 0, 0)

G = 0.05
AX = 0.1
AY = 0.1
BOUNCE = 0.5
STOP = 0.2
JUMP = 1.0
FRICTION = 0.95

# This global constant serves as a very useful convenience for me.
DIRECT_DICT = {pg.K_a  : (-AX, 0.0),
               pg.K_d : ( AX, 0.0),
               pg.K_w    : ( 0.0,-AY),
               pg.K_s  : ( 0.0, AY),
               pg.K_SPACE  : ( 0.0, -JUMP)
               }


class Player(object):
    """
    This class will represent our user controlled character.
    """
    SIZE = (100, 100)

    def __init__(self, pos, speed):
        """
        The pos argument is a tuple for the center of the player (x,y);
        speed is given in pixels/frame.
        """
        self.vx = 0.0
        self.vy = 0.0
        self.rect = pg.Rect((0,0), Player.SIZE)
        self.rect.center = pos
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = speed
        self.image = self.make_image()
        self.landed = False

    def make_image(self):
        """
        Creates our hero (a red circle with a black outline).
        """
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pg.draw.ellipse(image, pg.Color("black"), image_rect)
        pg.draw.ellipse(image, pg.Color("red"), image_rect.inflate(-12, -12))
        return image

    def update(self, keys, screen_rect):
        """
        Updates our player appropriately every frame.
        """
        if not self.landed:
            self.vy += G

        for key in DIRECT_DICT:
            if keys[key]:
                if not key == pg.K_SPACE or self.landed:
                    self.vx += DIRECT_DICT[key][0]*self.speed
                    self.vy += DIRECT_DICT[key][1]*self.speed
                    if key == pg.K_SPACE :
                        self.landed = False
        self.x += self.vx
        self.y += self.vy

        # Verifica se saiu da tela
        if not screen_rect.contains(self.rect):
            # Saiu pela esquerda?
            if self.x < 0 :
                self.vx = -self.vx * BOUNCE if abs(self.vx) + STOP else 0
                self.x = self.vx
            # Saiu pela direita?
            elif self.x > screen_rect.right - self.rect.width :
                self.vx = -self.vx * BOUNCE if abs(self.vx) + STOP else 0
                self.x = screen_rect.right - self.rect.width + self.vx
            # Saiu por cima?
            if self.y < 0 :
                #self.y -= self.vy
                self.vy = -self.vy * BOUNCE
                self.y =  self.vy
            # Saiu por baixo?
        elif round(self.y) >= screen_rect.bottom - self.rect.height and not self.landed:
                # Se velocidade baixa o suficiente, para
                if abs(self.vy) <= STOP:
                    self.y = screen_rect.bottom - self.rect.height
                    self.vy = 0.0
                    self.landed = True
                    print('** PARA **')
                # Se velocidade alta o suficiente, quica, com perda de velocidade
                else:
                    self.vy = -self.vy * BOUNCE
                    self.vx = self.vx * FRICTION
                    self.y = screen_rect.bottom - self.rect.height #+ self.vy
                    print('** QUICA **')

        # Se estiver no chão, aplica atrito
        if self.landed :
            self.vx = self.vx * FRICTION if abs(self.vx) > STOP else 0


            #self.rect.clamp_ip(screen_rect) # Keep player on screen.
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        # DEBUG
        #print(screen_rect,self.rect, self.x, self.y, self.vx, self.vy,self.landed)

    def draw(self, surface):
        """
        Blit image to the target surface.
        """
        surface.blit(self.image, self.rect)


class App(object):
    """
    A class to manage our event, game loop, and overall program flow.
    """
    def __init__(self):
        """
        Get a reference to the display surface; set up required attributes;
        and create a Player instance.
        """
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        self.player = Player(self.screen_rect.center, 5)

    def event_loop(self):
        """
        One event loop. Never cut your game off from the event loop.
        Your OS may decide your program has hung if the event queue is not
        accessed for a prolonged period of time.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                self.keys = pg.key.get_pressed()

    def render(self):
        """
        Perform all necessary drawing and update the screen.
        """
        self.screen.fill(pg.Color("white"))
        self.player.draw(self.screen)
        pg.display.update()

    def main_loop(self):
        """
        One game loop. Simple and clean.
        """
        while not self.done:
            self.event_loop()
            self.player.update(self.keys, self.screen_rect)
            self.render()
            self.clock.tick(self.fps)


def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
