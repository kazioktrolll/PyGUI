from main import Drawable, Vector2, AnyVector
from pygame import Color
import pygame
from math import sin, cos, atan, radians, degrees
import math
from multipledispatch import dispatch


class LineAbstract(object):
    def __init__(self, point1, point2):
        self.point1 = Vector2(point1)
        self.point2 = Vector2(point2)

    @classmethod
    def by_angle(cls, point, angle):
        # Angle in degrees
        point = Vector2(point)
        angle = radians(angle)
        point2 = point + Vector2(cos(angle), sin(angle))
        return cls(point, point2)

    @classmethod
    def by_equation(cls, a, b):
        # Equation given as 'ax + b = y'
        point1 = Vector2(b, 0)
        angle = degrees(atan(a))
        return cls.by_angle(point1, angle)

    def get_angle_rad(self):
        # Returns angle in radians
        dx = self.point1.x - self.point2.x
        dy = self.point1.y - self.point2.y
        return atan(dy / dx)

    def get_angle(self):
        # Returns angle in degrees
        return degrees(self.get_angle_rad())

    def get_equation(self):
        # Returns 'a', 'b' by format 'ax + b = y'
        x1, y1 = self.point1.tuple()
        x2, y2 = self.point2.tuple()
        a = (y1 - y2) / (x1 - x2)
        b = y1 - a * x1
        return a, b

    @dispatch(AnyVector)
    def get_distance(self, point):
        # Returns distance from a given point to the line
        point = Vector2(point)
        x1, y1 = self.point1.tuple()
        x2, y2 = self.point2.tuple()
        x0, y0 = point.tuple()

        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        distance = numerator / denominator

        return distance

    @dispatch('LineAbstract')
    def get_distance(self, line):
        a1, b1 = self.get_equation()
        a2, b2 = line.get_equation()

        if a1 != a2:
            raise ValueError('Lines must be parallel')

        return line.get_distance(self.point1)

    def get_crosspoint(self, line):
        a1, b1 = self.get_equation()
        a2, b2 = line.get_equation()

        if a1 == a2:
            raise ValueError('Lines must not be parallel')

        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1
        return x, y


class Line(Drawable):
    def __init__(self, display, point1, point2, isFinite=False, color=Color('#ffffff'), thickness=1):
        super().__init__(display=display, pos=point1)
        self.point1 = point1
        self.point2 = point2
        self.line = LineAbstract(point1, point2)

        self.isFinite = isFinite
        self.color = color
        self.thickness = thickness

    @classmethod
    def by_angle(cls, display, point, angle, color=Color('#ffffff'), thickness=1):
        line = LineAbstract.by_angle(point, angle)
        return cls(display=display, point1=line.point1, point2=line.point2, color=color, thickness=thickness)

    @classmethod
    def by_equation(cls, display, a, b, color=Color('#ffffff'), thickness=1):
        line = LineAbstract.by_equation(a, b)
        return cls(display=display, point1=line.point1, point2=line.point2, color=color, thickness=thickness)

    def find_render_borders(self, screen_size):
        w, h = screen_size
        points = [0, 0, 0, 0]
        try:
            points[0] = self.line.get_crosspoint(LineAbstract((0, 0), (0, h)))
        except ValueError:
            points[0] = None

        try:
            points[1] = self.line.get_crosspoint(LineAbstract((w, 0), (w, h)))
        except ValueError:
            points[1] = None

        try:
            points[3] = self.line.get_crosspoint(LineAbstract((0, 0), (w, 0)))
        except ValueError:
            points[3] = None

        try:
            points[4] = self.line.get_crosspoint(LineAbstract((0, h), (w, h)))
        except ValueError:
            points[4] = None

        points.remove(None)
        points.remove(None)

        return points

    def draw(self):
        if self.isFinite:
            pygame.draw.line(self.display, self.color, self.point1, self.point2, self.thickness)
            return None

        a, b = self.line.get_equation()
        point1 = Vector2(-10**3, a*-10**3 + b)
        point2 = Vector2(10**3, a*10**3 + b)
        pygame.draw.line(self.display, self.color, point1, point2, self.thickness)
        return None


__all__ = ('LineAbstract', 'Line')
