"""
Класс работы с базой данных (SQLite) для проекта "Треугольник".
"""
import sqlite3


class TriangleDatabase:
    """Хранит результаты расчетов треугольников, идентифицируемые тремя сторонами."""

    def __init__(self, db_path=":memory:"):
        self.connection = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS triangles (
                side_a TEXT NOT NULL,
                side_b TEXT NOT NULL,
                side_c TEXT NOT NULL,
                triangle_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                PRIMARY KEY (side_a, side_b, side_c)
            )
            """
        )
        self.connection.commit()

    def add_record(self, side_a, side_b, side_c, triangle_type, error_message=""):
        """Добавляет (или заменяет) запись о расчете треугольника."""
        self.connection.execute(
            "INSERT OR REPLACE INTO triangles (side_a, side_b, side_c, triangle_type, error_message) "
            "VALUES (?, ?, ?, ?, ?)",
            (str(side_a), str(side_b), str(side_c), triangle_type, error_message),
        )
        self.connection.commit()

    def get_record(self, side_a, side_b, side_c):
        """Возвращает словарь с записью или None, если записи нет."""
        cursor = self.connection.execute(
            "SELECT side_a, side_b, side_c, triangle_type, error_message "
            "FROM triangles WHERE side_a = ? AND side_b = ? AND side_c = ?",
            (str(side_a), str(side_b), str(side_c)),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            "side_a": row[0],
            "side_b": row[1],
            "side_c": row[2],
            "triangle_type": row[3],
            "error_message": row[4],
        }

    def delete_record(self, side_a, side_b, side_c):
        """Удаляет запись по трем сторонам. Возвращает True, если что-то было удалено."""
        cursor = self.connection.execute(
            "DELETE FROM triangles WHERE side_a = ? AND side_b = ? AND side_c = ?",
            (str(side_a), str(side_b), str(side_c)),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self):
        self.connection.close()
