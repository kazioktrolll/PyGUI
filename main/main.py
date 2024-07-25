import pygame
from typing import Union, Tuple


class Vector2(pygame.math.Vector2):
    def int(self):
        return int(self.x), int(self.y)

    def tuple(self):
        return self.x, self.y


class Game(object):
    def __init__(self, screenSize):
        pygame.init()

        self.display = pygame.display.set_mode(screenSize)
        self.clock = pygame.time.Clock()

        self.tickCall = lambda _: None
        self.drawCall = lambda: None
        self.eventCall = lambda _: None
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
            # Check if quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            self.eventCall(event)

    def exit(self):
        self.running = False

    @staticmethod
    def setCaption(caption):
        pygame.display.set_caption(caption)


class Drawable(object):
    def __init__(self, display, pos, hitbox=None):
        self.display = display
        self.pos = Vector2(pos)
        self.hitbox = hitbox
    
    def tick(self, dt):
        # Base tick function, called each tick. Uses 'dt' in milliseconds as time from previous tick
        raise NotImplementedError()

    def draw(self):
        # Returns surface to blit onto the display
        raise NotImplementedError()

    def moveTo(self, pos):
        self.pos = Vector2(pos)

    def moveBy(self, offset):
        self.pos += Vector2(offset)

    def isClicked(self, clickPos):
        if not self.hitbox:
            return False
        if clickPos[0] >= self.hitbox.get_width() or clickPos[1] >= self.hitbox.get_height():
            return False
        return self.hitbox.get_at(Vector2(clickPos - self.pos).int()) == (255, 255, 255, 255)


class Image(Drawable):
    def __init__(self, display, pos, image):
        super().__init__(display, pos)
        self.image = image

    def draw(self):
        return self.image


AnyVector = Union[Tuple[float, float], pygame.math.Vector2, Vector2]


__all__ = ["Vector2", "Game", "Drawable", "Image", "AnyVector"]

pygame.quit()
