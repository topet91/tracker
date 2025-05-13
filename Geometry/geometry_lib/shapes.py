from math import pi, sqrt
from abc import ABC, abstractmethod


class Shape(ABC):
    """Абстрактный базовый класс для геометрических фигур"""

    @abstractmethod
    def area(self) -> float:
        """Вычисляет площадь фигуры"""
        pass


class Circle(Shape):
    """Класс для работы с кругами"""

    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Радиус должен быть положительным числом")
        self.radius = radius

    def area(self) -> float:
        """Вычисляет площадь круга по формуле: S = πR**2"""
        return pi * self.radius ** 2


class Triangle(Shape):
    """Класс для работы с треугольниками"""

    def __init__(self, a: float, b: float, c: float):
        self._validate_sides(a, b, c)
        self.sides = sorted([a, b, c])
        self.a, self.b, self.c = self.sides

    def area(self) -> float:
        """Вычисляет площадь по формуле Герона"""
        s = (self.a + self.b + self.c) / 2
        return sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def is_right_angle(self, tolerance: float = 1e-8) -> bool:
        """Проверяет, является ли треугольник прямоугольным"""
        return abs(self.a ** 2 + self.b ** 2 - self.c ** 2) < tolerance

    @staticmethod
    def _validate_sides(a: float, b: float, c: float):
        """Валидация сторон треугольника"""
        if any(side <= 0 for side in (a, b, c)):
            raise ValueError("Все стороны должны быть положительными")
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Треугольник с такими сторонами не существует")


def calculate_area(shape: Shape) -> float:
    """Универсальная функция для вычисления площади"""
    return shape.area()
