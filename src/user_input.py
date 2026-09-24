"""
Класс взаимодействия с пользователем: интерфейс (ABC) + консольная реализация.
"""
from abc import ABC, abstractmethod


class UserInputInterface(ABC):
    """Абстрактный интерфейс получения входных данных от пользователя."""

    @abstractmethod
    def get_input(self):
        """Возвращает кортеж (side_a, side_b, side_c) как строки."""
        raise NotImplementedError


class ConsoleUserInput(UserInputInterface):
    """Реализация через стандартный консольный ввод."""

    def get_input(self):
        side_a = input("Введите длину стороны A: ")
        side_b = input("Введите длину стороны B: ")
        side_c = input("Введите длину стороны C: ")
        return side_a, side_b, side_c
