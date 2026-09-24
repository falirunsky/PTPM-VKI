import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from delivery_service import calculate_delivery_cost


class TestDeliveryValidation(unittest.TestCase):
    """Проверка граничных условий валидации веса, дистанции и типа посылки."""

    def test_weight_below_minimum_is_rejected(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_weight_at_minimum_boundary_is_accepted(self):
        cost, _ = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_weight_at_maximum_boundary_is_accepted(self):
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_weight_above_maximum_is_rejected(self):
        cost, date = calculate_delivery_cost(50.01, 100, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_distance_below_minimum_is_rejected(self):
        cost, date = calculate_delivery_cost(1, 0, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_distance_at_maximum_boundary_is_accepted(self):
        cost, _ = calculate_delivery_cost(1, 5000, "обычный")
        self.assertNotEqual(cost, -1)

    def test_distance_above_maximum_is_rejected(self):
        cost, date = calculate_delivery_cost(1, 5001, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_invalid_package_type_is_rejected(self):
        cost, date = calculate_delivery_cost(1, 100, "неизвестный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))


class TestDeliveryCostCalculation(unittest.TestCase):
    """Проверка расчета стоимости для базовых сценариев и весовых коэффициентов."""

    def test_base_cost_light_package(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)  # (200 + 100*5) без надбавок

    def test_weight_tier_5_to_20_kg_applies_1_2_multiplier(self):
        # Ожидается: посылка весом РОВНО 5 кг должна попадать в тариф "5–20 кг" (x1.2)
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 840)  # (200 + 500) * 1.2

    def test_weight_just_above_5_kg_applies_1_2_multiplier(self):
        cost, _ = calculate_delivery_cost(5.1, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_tier_over_20_kg_applies_1_5_multiplier(self):
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)  # (200 + 500) * 1.5

    def test_fragile_package_adds_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий")
        self.assertEqual(cost, 1000)  # 700 + 300

    def test_dangerous_package_adds_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "опасный")
        self.assertEqual(cost, 1700)  # 700 + 1000

    def test_express_delivery_increases_cost_not_decreases(self):
        # Ожидается: экспресс-доставка должна быть ДОРОЖЕ обычной, а не дешевле
        normal_cost, _ = calculate_delivery_cost(1, 100, "обычный", False)
        express_cost, _ = calculate_delivery_cost(1, 100, "обычный", True)
        self.assertGreater(express_cost, normal_cost)


class TestDeliveryDateCalculation(unittest.TestCase):
    """Проверка расчета сроков доставки."""

    def test_short_distance_gives_minimum_one_day(self):
        _, date = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_thousand_km_gives_two_days(self):
        _, date = calculate_delivery_cost(1, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_express_delivery_never_arrives_same_day_as_dispatch(self):
        # Ожидается: даже экспресс-доставка не может занимать 0 дней
        _, date = calculate_delivery_cost(1, 100, "обычный", True)
        self.assertNotEqual(date, "2026-09-03")

    def test_max_distance_delivery_date(self):
        _, date = calculate_delivery_cost(1, 5000, "обычный")
        self.assertEqual(date, "2026-09-13")


if __name__ == "__main__":
    unittest.main()
