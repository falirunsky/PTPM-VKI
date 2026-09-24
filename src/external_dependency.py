"""
Класс сторонней зависимости: интерфейс (ABC) + имитация отправки данных
(например, на email-сервер).
"""
import logging
from abc import ABC, abstractmethod


class ExternalDependencyInterface(ABC):
    """Абстрактный интерфейс отправки строки-результата стороннему процессу."""

    @abstractmethod
    def send(self, message):
        """Отправляет message стороннему процессу. Возвращает True при успехе."""
        raise NotImplementedError


class EmailNotifier(ExternalDependencyInterface):
    """Имитация отправки результата на email-сервер (без реального сетевого вызова)."""

    def send(self, message):
        logging.info("Имитация отправки на email-сервер: %s", message)
        return True
