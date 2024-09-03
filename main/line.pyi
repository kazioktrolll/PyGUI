import pygame
from .main import Drawable, Vector2, AnyVector
from pygame import Color
from typing import Tuple


class LineMathematical(object):
    def __init__(self, point1: AnyVector, point2: AnyVector) -> LineMathematical:
        self.point1: Vector2 = None
        self.point2: Vector2 = None
        ...
    @classmethod
    def by_angle(cls, point: AnyVector, angle: float) -> LineMathematical: ...
    @classmethod
    def by_equation(cls, a: float, b: float) -> LineMathematical: ...
    def get_angle_rad(self) -> float: ...
    def get_angle(self) -> float: ...
    def get_equation(self) -> Tuple[float, float]: ...
    def get_distance(self, point: AnyVector) -> float: ...
    def get_crosspoint(self, line: LineMathematical) -> Tuple[float, float]: ...


class Line(Drawable):
    def __init__(self, display: pygame.Surface, point1: AnyVector, point2: AnyVector,
                 color: Color = None, thickness: int = None):
        super().__init__(display=display, pos=point1)
        self.point1: Vector2 = None
        self.point2: Vector2 = None
        self.line: LineMathematical = None

        self.is_finite: bool = None
        self.color: Color = None
        self.thickness: int = None
    @classmethod
    def by_angle(cls, display: pygame.Surface, point: AnyVector, angle: float, color: Color = None,
                 thickness: int = None) -> Line: ...
    @classmethod
    def by_equation(cls, display: pygame.Surface, a: float, b: float, color: Color = None,
                    thickness: int = None) -> Line: ...
    def find_render_borders(self, screen_size: Tuple[int, int]) -> Tuple[AnyVector, AnyVector]: ...

class HalfLine(Line):
    def __init__(self, display: pygame.Surface, point1: AnyVector, point2: AnyVector,
                 color: Color = None, thickness: int = None):
        super().__init__(display=display, point1=point1, point2=point2, color=color, thickness=thickness)
        ...

class Segment(Drawable):
    def __init__(self, display: pygame.Surface, point1: AnyVector, point2: AnyVector,
                 color: Color = None, thickness: int = None):
        self.point1: Vector2 = None
        self.point2: Vector2 = None
        self.color: Color = None
        self.thickness: int = None
        ...
