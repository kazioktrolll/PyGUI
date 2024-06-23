import pygame
from typing import Any, Optional


class Game(object):
    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode((1000, 500))
        self.clock = pygame.time.Clock()

        self.tickCall:callable[[int], None] = lambda _: None
        self.drawCall:callable[[], None] = lambda: None

        self.running:bool = True
        while self.running:
            self.tick()
        
    def tick(self) -> None:
        dt:int = self.clock.tick()
        self.handleEvents()
        self.tickCall(dt)
        self.draw()

    def draw(self) -> None:
        self.display.fill('#000000')
        self.drawCall()
        pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key in EVENTDICT.keys():
                    EVENTDICT[event.key]()

    def exit(self) -> None:
        self.running = False


EVENTDICT:dict[int, Any] = {
}


if __name__ == "__main__":
    Game()
