import unittest
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang tinh tien don hang."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}

        result = self.app.calculate_order_total(cart)

        self.assertEqual(result, 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}

        result = self.app.calculate_order_total(cart)

        self.assertEqual(result, 95000)

    def test_calculate_total_for_empty_cart(self):
        result = self.app.calculate_order_total({})

        self.assertEqual(result, 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}

        result = self.app.calculate_order_total(cart)

        self.assertEqual(result, 0.0)


if __name__ == "__main__":
    unittest.main()