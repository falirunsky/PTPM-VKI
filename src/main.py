"""
Точка входа: собирает все классы Лабораторной работы №3 в единый сценарий.
"""
import logging
import os
import sys

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
    ],
)

from controller import Controller
from database import TriangleDatabase
from external_dependency import EmailNotifier
from triangle_calculator import TriangleCalculator
from user_input import ConsoleUserInput

if __name__ == "__main__":
    calculator = TriangleCalculator()
    database = TriangleDatabase("triangles.db")
    user_input = ConsoleUserInput()
    notifier = EmailNotifier()

    controller = Controller(calculator, database, user_input, notifier)
    outcome = controller.run()

    print(outcome)

    database.close()
