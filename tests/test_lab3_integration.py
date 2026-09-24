import os
import sys
import unittest
from abc import ABC
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from controller import Controller
from database import TriangleDatabase
from external_dependency import EmailNotifier, ExternalDependencyInterface
from triangle_calculator import TriangleCalculator
from user_input import ConsoleUserInput, UserInputInterface


class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        self.database = TriangleDatabase(":memory:")
        self.calculator = TriangleCalculator()

    def tearDown(self):
        self.database.close()

    def test_new_triangle_is_calculated_saved_and_sent(self):
        """Данных в БД нет -> контроллер считает, сохраняет запись и отправляет её."""
        user_input = MagicMock(spec=UserInputInterface)
        user_input.get_input.return_value = ("5", "5", "5")

        notifier = MagicMock(spec=ExternalDependencyInterface)

        controller = Controller(self.calculator, self.database, user_input, notifier)
        result = controller.run()

        self.assertEqual(result["triangle_type"], "равносторонний")
        self.assertEqual(result["error_message"], "")

        saved = self.database.get_record("5", "5", "5")
        self.assertIsNotNone(saved)
        self.assertEqual(saved["triangle_type"], "равносторонний")

        notifier.send.assert_called_once()
        sent_message = notifier.send.call_args[0][0]
        self.assertIn("равносторонний", sent_message)

    def test_existing_record_is_taken_from_db_without_recalculation(self):
        """Данные уже есть в БД -> контроллер не должен пересчитывать значение."""
        self.database.add_record("3", "4", "5", "разносторонний", "")

        user_input = MagicMock(spec=UserInputInterface)
        user_input.get_input.return_value = ("3", "4", "5")

        fake_calculator = MagicMock(spec=TriangleCalculator)
        notifier = MagicMock(spec=ExternalDependencyInterface)

        controller = Controller(fake_calculator, self.database, user_input, notifier)
        result = controller.run()

        self.assertEqual(result["triangle_type"], "разносторонний")
        fake_calculator.calculate.assert_not_called()
        notifier.send.assert_called_once()

    def test_invalid_input_is_stored_with_error_and_reported(self):
        """Нечисловой ввод -> ошибка сохраняется в БД и передается зависимости."""
        user_input = MagicMock(spec=UserInputInterface)
        user_input.get_input.return_value = ("abc", "4", "5")

        notifier = MagicMock(spec=ExternalDependencyInterface)

        controller = Controller(self.calculator, self.database, user_input, notifier)
        result = controller.run()

        self.assertEqual(result["triangle_type"], "")
        self.assertNotEqual(result["error_message"], "")

        saved = self.database.get_record("abc", "4", "5")
        self.assertIsNotNone(saved)
        self.assertNotEqual(saved["error_message"], "")

        sent_message = notifier.send.call_args[0][0]
        self.assertIn("Ошибка", sent_message)

    def test_degenerate_triangle_flow_end_to_end(self):
        """Стороны не образуют треугольник -> корректно проходит весь сценарий."""
        user_input = MagicMock(spec=UserInputInterface)
        user_input.get_input.return_value = ("1", "2", "3")

        notifier = MagicMock(spec=ExternalDependencyInterface)

        controller = Controller(self.calculator, self.database, user_input, notifier)
        result = controller.run()

        self.assertEqual(result["triangle_type"], "не треугольник")
        saved = self.database.get_record("1", "2", "3")
        self.assertIsNotNone(saved)
        notifier.send.assert_called_once()


# ---------------------------------------------------------------------------
# Модульные тесты: работа с БД в изоляции.
# ---------------------------------------------------------------------------

class TestTriangleDatabase(unittest.TestCase):

    def setUp(self):
        self.database = TriangleDatabase(":memory:")

    def tearDown(self):
        self.database.close()

    def test_add_and_get_record_roundtrip(self):
        self.database.add_record("3", "4", "5", "разносторонний", "")
        record = self.database.get_record("3", "4", "5")
        self.assertEqual(record["triangle_type"], "разносторонний")
        self.assertEqual(record["error_message"], "")

    def test_get_nonexistent_record_returns_none(self):
        record = self.database.get_record("100", "200", "300")
        self.assertIsNone(record)

    def test_delete_record_removes_entry(self):
        self.database.add_record("5", "5", "5", "равносторонний", "")
        deleted = self.database.delete_record("5", "5", "5")
        self.assertTrue(deleted)
        self.assertIsNone(self.database.get_record("5", "5", "5"))

    def test_delete_nonexistent_record_returns_false(self):
        deleted = self.database.delete_record("42", "42", "42")
        self.assertFalse(deleted)

    def test_add_record_overwrites_existing_entry(self):
        self.database.add_record("6", "6", "6", "равносторонний", "")
        self.database.add_record("6", "6", "6", "исправлено", "тестовая ошибка")
        record = self.database.get_record("6", "6", "6")
        self.assertEqual(record["triangle_type"], "исправлено")
        self.assertEqual(record["error_message"], "тестовая ошибка")


# ---------------------------------------------------------------------------
# Модульные тесты: интерфейсы (ABC) и их конкретные реализации, с заглушками
# для input() и имитации сторонней зависимости.
# ---------------------------------------------------------------------------

class TestUserInputInterface(unittest.TestCase):

    def test_user_input_interface_cannot_be_instantiated_directly(self):
        self.assertTrue(issubclass(UserInputInterface, ABC))
        with self.assertRaises(TypeError):
            UserInputInterface()

    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_console_user_input_reads_three_values_in_order(self, mock_input):
        console_input = ConsoleUserInput()
        result = console_input.get_input()
        self.assertEqual(result, ("3", "4", "5"))
        self.assertEqual(mock_input.call_count, 3)


class TestExternalDependencyInterface(unittest.TestCase):

    def test_external_dependency_interface_cannot_be_instantiated_directly(self):
        self.assertTrue(issubclass(ExternalDependencyInterface, ABC))
        with self.assertRaises(TypeError):
            ExternalDependencyInterface()

    def test_email_notifier_send_returns_true_without_network_call(self):
        notifier = EmailNotifier()
        result = notifier.send("тестовое сообщение")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
