from .main import Drawable, Vector2, Color
import pygame


pygame.font.init()


class Text(Drawable):
    def __init__(self, display, position, text='', font=pygame.font.SysFont('Arial', 20),
                 font_color=Color('#ffffff'), hitbox=None):
        super().__init__(display, position, hitbox)
        self.text = text
        self.font = font
        self.font_color = font_color

    def draw(self):
        return self.render_text(self.font_color)

    def get_text_lines_surfaces(self, font_color):
        # Returns a list of surfaces, one for every line of text rendered

        FONT = self.font
        # Split the text into lines
        lines = self.text.split('\n')
        surfaces = [FONT.render(line, True, font_color) for line in lines]
        return surfaces

    def render_text(self, font_color=Color('#ffffff')):
        # Returns a surface with the text rendered on it

        surfaces = self.get_text_lines_surfaces(font_color)

        total_height = sum(surface.get_height() for surface in surfaces)
        max_width = max(surface.get_width() for surface in surfaces)
        surface = pygame.Surface((max_width, total_height))

        y = 0
        for line_surface in surfaces:
            surface.blit(line_surface, self.position + Vector2(0, y))
            y += line_surface.get_height()
        return surface

    def set_auto_hitbox(self):
        surfaces = self.get_text_lines_surfaces()

        total_height = sum(surface.get_height() for surface in surfaces)
        max_width = max(surface.get_width() for surface in surfaces)
        surface = pygame.Surface((max_width, total_height))

        surface.fill('#000000')
        h = 0
        for i in range(len(surfaces)):
            surface.fill('#ffffff', pygame.Rect(0, h, surfaces[i].get_width(), surfaces[i].get_height()))
            h += surfaces[i].get_height()

        self.hitbox = surface


    def write(self, text):
        # Sets the input as new text
        self.text = text

    def clear(self):
        # Clears the text completely
        self.text = ''


class TextBox(Text):
    def __init__(self, display, position, font=pygame.font.SysFont('Arial', 20), font_color=Color('#ffffff'),
                 font_color_active=Color('#00ff00'), flexible_hitbox=True):
        super().__init__(display, position, text="", font=font, font_color=font_color)
        self.is_active = False
        self.true_text = ""
        self.font_color_active = font_color_active
        self.flexible_hitbox = flexible_hitbox

    def type_text(self, char, key):
        # Append the text with input
        def backspace():
            self.text = self.text[:-1]

        def new_line():
            self.text += "\n"

        special_keys = {
            pygame.K_BACKSPACE: backspace,
            pygame.K_RETURN: new_line
        }

        if key in special_keys:
            special_keys[key]()
            return None

        self.text += char

    def handle_events(self, event):
        if not self.is_active:
            return None
        if event.type != pygame.KEYDOWN:
            return None

        self.type_text(event.unicode, event.key)

    def draw(self):
        color = self.font_color if not self.is_active else self.font_color_active
        displayed_text = self.render_text(color)
        if self.flexible_hitbox:
            self.set_auto_hitbox()
        return displayed_text


pygame.font.quit()

__all__ = ['Text', 'TextBox']
