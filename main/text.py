from .main import Drawable, Vector2
import pygame


pygame.font.init()


class Text(Drawable):
    def __init__(self, display, pos, text='', font=pygame.font.SysFont('Arial', 20), font_color='#ffffff',
                 hitbox=None):
        super().__init__(display, pos, hitbox)
        self.text = text
        self.font = font
        self.font_color = font_color

    def draw(self):
        return self.render_text(self.font_color)

    def render_text(self, font_color='#ffffff'):
        FONT = self.font
        # Split the text into lines
        lines = self.text.split('\n')
        surfaces = [FONT.render(line, True, font_color) for line in lines]

        total_height = sum(surface.get_height() for surface in surfaces)
        max_width = max(surface.get_width() for surface in surfaces)
        surface = pygame.Surface((max_width, total_height))

        y = 0
        for line_surface in surfaces:
            surface.blit(line_surface, self.pos + Vector2(0, y))
            y += line_surface.get_height()
        return surface

    def set_auto_hitbox(self):
        self.hitbox = pygame.Surface(self.render_text().get_size())
        self.hitbox.fill('#ffffff')

    def write(self, text):
        self.text = text

    def clear(self):
        self.text = ''


class TextBox(Text):
    def __init__(self, display, pos, font=pygame.font.SysFont('Arial', 20), font_color='#ffffff',
                 font_color_active='#00ff00', flexible_hitbox=True):
        super().__init__(display, pos, text="", font=font, font_color=font_color)
        self.is_active = False
        self.true_text = ""
        self.font_color_active = font_color_active
        self.flexible_hitbox = flexible_hitbox

    def type(self, char, key):
        def backspace():
            self.text = self.text[:-1]

        def new_line():
            self.text += "\n"

        special_keys = {pygame.K_BACKSPACE: backspace, pygame.K_RETURN: new_line}
        if key in special_keys:
            special_keys[key]()
            return None

        self.text += char

    def handle_events(self, event):
        if not self.is_active:
            return None
        if event.type != pygame.KEYDOWN:
            return None

        self.type(event.unicode, event.key)

    def draw(self):
        color = self.font_color if not self.is_active else self.font_color_active
        dispText = self.render_text(color)
        if self.flexible_hitbox:
            self.set_auto_hitbox()
        return dispText


pygame.font.quit()

__all__ = ['Text', 'TextBox']
