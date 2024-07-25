from .main import Drawable, AnyVector, Color, Event
import pygame


class Text(Drawable):
    def __init__(self, display:pygame.Surface, pos: AnyVector, text: str = "", font: pygame.font.Font = None,
                 fontColor: Color = None, hitbox: pygame.Surface = None
                 ) -> None:
        self.font: pygame.font.Font = None
        self.text: str = None
        self.fontColor: Color = None
        self.hitbox: pygame.Surface = None
        ...
    def draw(self) -> pygame.Surface: ...
    def renderText(self, color: Color = None) -> pygame.Surface: ...
    def setAutoHitbox(self) -> None: ...
    def write(self, text: str) -> None: ...
    def clear(self) -> None: ...

class TextBox(Text):
    def __init__(self, display: pygame.Surface, pos: AnyVector, font: pygame.font.Font = None,
                 fontColor: Color = None, fontColorActive: Color = None,
                 flexibleHitbox: bool = None) -> None:
        self.isActive: bool = None
        self.trueText: str = None
        self.fontColorActive: Color = None
        self.flexibleHitbox: bool = None
        ...
    def type(self, char:str, key: int) -> None: ...
    def handleEvents(self, event: Event) -> None: ...
    def draw(self) -> pygame.Surface: ...
