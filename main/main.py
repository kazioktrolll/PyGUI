import pygame


class Game(object):
    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode((1000, 500))

        self.running:bool = True
        while self.running:
            self.tick()

if __name__ == "__main__":
    Game()