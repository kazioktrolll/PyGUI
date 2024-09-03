import pygame
from typing import Union, Tuple


class Vector2(pygame.math.Vector2):
    def get_intiger_xy(self):
        return int(self.x), int(self.y)

    def get_xy(self):
        return self.x, self.y


class Game(object):
    def __init__(self, screen_size):
        pygame.init()

        self.display = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()

        self.tick_callabe = lambda _: None
        self.draw_callable = lambda: None
        self.event_callable = lambda _: None
        self.is_running: bool = False

    def run(self):
        self.is_running: bool = True
        while self.is_running:
            self.tick()

    def tick(self):
        frame_time_difference_milliseconds: int = self.clock.tick()
        self.handle_events()
        self.tick_callabe(frame_time_difference_milliseconds)
        self.draw()

    def draw(self):
        self.display.fill('#000000')
        self.draw_callable()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            # Check if quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.is_running = False
                return None

            self.event_callable(event)

    def exit(self):
        self.is_running = False

    @staticmethod
    def set_caption(caption):
        pygame.display.set_caption(caption)

    def quick_render(self, list_of_drawables):
        for drawable in list_of_drawables:
            image = drawable.draw()
            position = drawable.pos + drawable.draw_offset()
            self.display.blit(image, position)


class Drawable(object):
    def __init__(self, display, position, hitbox=None):
        self.display = display
        self.position = Vector2(position)
        self.hitbox = hitbox
    
    def tick(self, dt):
        # Base tick function, called each tick. Uses 'dt' in milliseconds as time from previous tick
        raise NotImplementedError()

    def draw(self):
        # Returns surface to blit onto the display
        raise NotImplementedError()

    def draw_offset(self):
        # Used when coordinate used to display the object is different from Drawable.pos. (0, 0) by default
        return Vector2(0, 0)

    def move_to(self, position):
        self.position = Vector2(position)

    def move_by(self, offset):
        self.position += Vector2(offset)

    def is_clicked(self, click_position):
        if not self.hitbox:
            return False
        if click_position[0] >= self.hitbox.get_width() or click_position[1] >= self.hitbox.get_height():
            return False
        return self.hitbox.get_at(Vector2(click_position - self.position).get_intiger_xy()) == (255, 255, 255, 255)


class Image(Drawable):
    def __init__(self, display, position, image):
        super().__init__(display, position)
        self.image = image

    def draw(self):
        return self.image


AnyVector = Union[Tuple[float, float], pygame.math.Vector2, Vector2]


__all__ = ["Vector2", "Game", "Drawable", "Image", "AnyVector", "pygame"]

pygame.quit()
