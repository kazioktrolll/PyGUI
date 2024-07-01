import pygame
from typing import Callable


class Vector2(pygame.math.Vector2):
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

    @staticmethod
    def setCaption(caption):
        pygame.display.set_caption(caption)


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


pygame.font.init()


class Text(Drawable):
    def __init__(self, display, pos, text='', font=pygame.font.SysFont('Arial', 20), fontColor='#ffffff'):
        super().__init__(display, pos)
        self.text = text
        self.font = font
        self.fontColor = fontColor

    def draw(self):
        dispText = self.font.render(self.text, True, self.fontColor)
        self.display.blit(dispText, self.pos.int())

    def write(self, text):
        self.text = text

    def clear(self):
        self.text = ''


class TextBox(Text):
    def __init__(self, display, pos, font=pygame.font.SysFont('Arial', 20), fontColor='#ffffff',
                 fontColorActive = '#00ff00'):
        super().__init__(display, pos, "", font, fontColor)
        self.isActive = False
        self.trueText = ""
        self.fontColorActive = fontColorActive

    def type(self, char):
        def backspace():
            self.text = self.text[:-1]

        def newLine():
            self.text += "\n"

        specialKeys = {'08': backspace, '13': newLine}
        if char in specialKeys:
            specialKeys[char]()
            return None

        self.text += char

    def draw(self):
        color = self.fontColor if not self.isActive else self.fontColorActive
        dispText = self.font.render(self.text, True, color)
        self.display.blit(dispText, self.pos.int())


__all__ = ["Vector2", "Game", "Drawable", "Image", "TextBox", "EVENTDICT", "KEYDOWNDICT"]
