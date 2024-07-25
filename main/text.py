from .main import Drawable, Vector2
import pygame


pygame.font.init()


class Text(Drawable):
    def __init__(self, display, pos, text='', font=pygame.font.SysFont('Arial', 20), fontColor='#ffffff',
                 hitbox=None):
        super().__init__(display, pos, hitbox)
        self.text = text
        self.font = font
        self.fontColor = fontColor

    def draw(self):
        dispText = self.renderText(self.fontColor)
        self.display.blit(dispText, self.pos.int())

    def renderText(self, fontColor='#ffffff'):
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

    def setAutoHitbox(self):
        self.hitbox = pygame.Surface(self.renderText().get_size())
        self.hitbox.fill('#ffffff')

    def write(self, text):
        self.text = text

    def clear(self):
        self.text = ''


class TextBox(Text):
    def __init__(self, display, pos, font=pygame.font.SysFont('Arial', 20), fontColor='#ffffff',
                 fontColorActive='#00ff00', flexibleHitbox=True):
        super().__init__(display, pos, text="", font=font, fontColor=fontColor)
        self.isActive = False
        self.trueText = ""
        self.fontColorActive = fontColorActive
        self.flexibleHitbox = flexibleHitbox

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
            return None
        if event.type != pygame.KEYDOWN:
            return None

        self.type(event.unicode, event.key)

    def draw(self):
        color = self.fontColor if not self.isActive else self.fontColorActive
        dispText = self.renderText(color)
        if self.flexibleHitbox:
            self.setAutoHitbox()
        self.display.blit(dispText, self.pos.int())


pygame.font.quit()

__all__ = ['Text', 'TextBox']
