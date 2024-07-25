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

        self.tick_call = lambda _: None
        self.draw_call = lambda: None
        self.event_call = lambda _: None
        self.running: bool = False

    def run(self):
        self.running: bool = True
        while self.running:
            self.tick()

    def tick(self):
        dt: int = self.clock.tick()
        self.handle_events()
        self.tick_call(dt)
        self.draw()

    def draw(self):
        self.display.fill('#000000')
        self.draw_call()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            # Check if quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

            self.event_call(event)

    def exit(self):
        self.running = False

    @staticmethod
    def set_caption(caption):
        pygame.display.set_caption(caption)

    def quick_render(self, list_of_drawables):
        for drawable in list_of_drawables:
            image = drawable.draw()
            pos = drawable.pos
            self.display.blit(image, pos)


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

    def move_to(self, pos):
        self.pos = Vector2(pos)

    def move_by(self, offset):
        self.pos += Vector2(offset)

    def is_clicked(self, click_pos):
        if not self.hitbox:
            return False
        if click_pos[0] >= self.hitbox.get_width() or click_pos[1] >= self.hitbox.get_height():
            return False
        return self.hitbox.get_at(Vector2(click_pos - self.pos).int()) == (255, 255, 255, 255)


class Image(Drawable):
    def __init__(self, display, pos, image):
        super().__init__(display, pos)
        self.image = image

    def draw(self):
        return self.image


AnyVector = Union[Tuple[float, float], pygame.math.Vector2, Vector2]


__all__ = ["Vector2", "Game", "Drawable", "Image", "AnyVector"]

pygame.quit()
