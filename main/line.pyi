import pygame

from main import Drawable, Vector2, AnyVector
from pygame import Color
from multipledispatch import dispatch
from typing import Tuple


class LineAbstract(object):
    def __init__(self, point1: AnyVector, point2: AnyVector) -> LineAbstract:
        self.point1: Vector2 = None
        self.point2: Vector2 = None
        ...
    @classmethod
    def by_angle(cls, point: AnyVector, angle: float) -> LineAbstract: ...
    @classmethod
    def by_equation(cls, a: float, b: float) -> LineAbstract: ...
    def get_angle_rad(self) -> float: ...
    def get_angle(self) -> float: ...
    def get_equation(self) -> Tuple[float, float]: ...
    @dispatch(Vector2)
    def get_distance(self, point: AnyVector) -> float: ...
    @dispatch('LineAbstract')
    def get_distance(self, line: LineAbstract) -> float: ...
    def get_crosspoint(self, line: LineAbstract) -> Tuple[float, float]: ...


class Line(Drawable):
    def __init__(self, display: pygame.Surface, point1: AnyVector, point2: AnyVector, isFinite: bool=None,
                 color: Color = None, thickness: int = None):
        super().__init__(display=display, pos=point1)
        self.point1: Vector2 = None
        self.point2: Vector2 = None
        self.line: LineAbstract = None

        self.isFinite: bool = None
        self.color: Color = None
        self.thickness: int = None
    @classmethod
    def by_angle(cls, display: pygame.Surface, point: AnyVector, angle: float, color: Color = None,
                 thickness: int = None) -> Line: ...
    @classmethod
    def by_equation(cls, display: pygame.Surface, a: float, b: float, color: Color = None,
                    thickness: int = None) -> Line: ...
    def find_render_borders(self, screen_size: Tuple[int, int]) -> Tuple[AnyVector, AnyVector]: ...
    def draw(self) -> None: ...
