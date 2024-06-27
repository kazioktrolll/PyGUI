import pygame
from pygame.math import Vector2 as V2
from typing import Callable


class Vector2(V2):
    def int(self):
        return Vector2(int(self.x), int(self.y))


EVENTDICT = {}
KEYDOWNDICT = {}


class Game(object):
    def __init__(self, screenSize):
        pygame.init()

        self.display = pygame.display.set_mode(screenSize)
        self.clock = pygame.time.Clock()

        self.tickCall: Callable[[int], None] = lambda _: None
        self.drawCall: Callable[[], None] = lambda: None
        self.eventDict = EVENTDICT
        self.keyDownDict = KEYDOWNDICT
        self.running: bool = False

    def run(self):
        self.running: bool = True
        while self.running:
            self.tick()
        
    def tick(self):
        dt: int = self.clock.tick()
        self.handleEvents()
        self.tickCall(dt)
        self.draw()

    def draw(self):
        self.display.fill('#000000')
        self.drawCall()
        pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            if event.type in self.eventDict:
                self.eventDict[event.type]()

            if event.type == pygame.KEYDOWN:
                if event.key in self.eventDict.keys():
                    self.eventDict[event.key]()

    def exit(self):
        self.running = False


class Drawable(object):
    def __init__(self, display, pos):
        self.display = display
        self.pos = Vector2(pos)
    
    def tick(self, dt):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()

    def moveTo(self, pos):
        self.pos = Vector2(pos)

    def moveBy(self, offset):
        self.pos += Vector2(offset)


class Image(Drawable):
    def __init__(self, display, pos, image):
        super().__init__(display, pos)
        self.image = image

    def draw(self):
        self.display.blit(self.image, self.pos.int())


__all__ = ["Vector2", "Game", "Drawable", "Image", "EVENTDICT", "KEYDOWNDICT"]
