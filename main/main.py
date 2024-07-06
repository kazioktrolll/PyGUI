import pygame


class Vector2(pygame.math.Vector2):
    def int(self):
        return Vector2(int(self.x), int(self.y))


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
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()

    def moveTo(self, pos):
        self.pos = Vector2(pos)

    def moveBy(self, offset):
        self.pos += Vector2(offset)

    def isClicked(self, clickPos):
        return self.hitbox.get_at((clickPos - self.pos).int()) == '#ffffff'


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

    def renderText(self, fontColor):
        FONT = self.font
        # Split the text into lines
        lines = self.text.split('\n')
        surfaces = [FONT.render(line, True, fontColor) for line in lines]

        total_height = sum(surface.get_height() for surface in surfaces)
        max_width = max(surface.get_width() for surface in surfaces)
        surface = pygame.Surface((max_width, total_height))

        y = 0
        for line_surface in surfaces:
            surface.blit(line_surface, self.pos + Vector2(0, y))
            y += line_surface.get_height()
        return surface

    def draw(self):
        dispText = self.renderText(self.fontColor)
        self.display.blit(dispText, self.pos.int())

    def write(self, text):
        self.text = text

    def clear(self):
        self.text = ''


class TextBox(Text):
    def __init__(self, display, pos, font=pygame.font.SysFont('Arial', 20), fontColor='#ffffff',
                 fontColorActive='#00ff00'):
        super().__init__(display, pos, "", font, fontColor)
        self.isActive = False
        self.trueText = ""
        self.fontColorActive = fontColorActive

    def type(self, char, key):
        def backspace():
            self.text = self.text[:-1]

        def newLine():
            self.text += "\n"

        specialKeys = {pygame.K_BACKSPACE: backspace, pygame.K_RETURN: newLine}
        if key in specialKeys:
            specialKeys[key]()
            return None

        self.text += char

    def handleEvents(self, event):
        if not self.isActive:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.isClicked(event.pos):
                self.isActive = True
            return None

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE:
            self.isActive = False
            return None
        self.type(event.unicode, event.key)

    def draw(self):
        color = self.fontColor if not self.isActive else self.fontColorActive
        dispText = self.renderText(color)
        self.display.blit(dispText, self.pos.int())


__all__ = ["Vector2", "Game", "Drawable", "Image", "Text", "TextBox"]

pygame.font.quit()
pygame.quit()


if __name__ == '__main__':
    g = Game((300, 300))
    tb = TextBox(g.display, (0, 0))
    tb.write("Hello World!")
    tb.font = pygame.font.SysFont('Arial', 20)
    tb.isActive = True
    g.drawCall = tb.draw
    g.eventCall = tb.handleEvents
    g.run()
