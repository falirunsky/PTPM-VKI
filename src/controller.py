"""
Класс-контроллер, объединяющий вычисления, БД, ввод пользователя и стороннюю
зависимость в единый сквозной сценарий.
"""
import logging


class Controller:
    def __init__(self, calculator, database, user_input, notifier):
        self.calculator = calculator
        self.database = database
        self.user_input = user_input
        self.notifier = notifier

    def run(self):
        """
        Сквозной сценарий:
        1. Получить данные от пользователя
        2. Если записи в БД нет, то вычислить и сохранить; если есть, то взять из бд
        3. Отправить результат сторонней зависимости
        4. Вернуть результат
        """
        side_a, side_b, side_c = self.user_input.get_input()

        existing = self.database.get_record(side_a, side_b, side_c)

        if existing is None:
            tri_type, _coords, error_message = self.calculator.calculate(side_a, side_b, side_c)
            self.database.add_record(side_a, side_b, side_c, tri_type, error_message)
            triangle_type = tri_type
        else:
            logging.info("Найдена запись в БД для (%s, %s, %s)", side_a, side_b, side_c)
            triangle_type = existing["triangle_type"]
            error_message = existing["error_message"]

        if error_message:
            result_message = f"Ошибка для ({side_a}, {side_b}, {side_c}): {error_message}"
        else:
            result_message = f"Треугольник ({side_a}, {side_b}, {side_c}) -> {triangle_type}"

        self.notifier.send(result_message)

        return {
            "side_a": side_a,
            "side_b": side_b,
            "side_c": side_c,
            "triangle_type": triangle_type,
            "error_message": error_message,
        }
