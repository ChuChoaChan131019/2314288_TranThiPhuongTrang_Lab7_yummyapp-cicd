import unittest
from unittest.mock import patch

import gps_service
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


class TestMediumLevel(unittest.TestCase):
    """Kiem thu ma khuyen mai."""

    def test_apply_valid_promo_online(self):
        app = YummyApp(network_status="online")
        result = app.apply_promo_code(100000, "GIAM10")
        self.assertEqual(result, 90000)

    def test_apply_promo_when_offline(self):
        app = YummyApp(network_status="offline")

        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_apply_new_os_promo_on_os_15(self):
        app = YummyApp(os_version=15)
        result = app.apply_promo_code(100000, "NEW_OS_ONLY")
        self.assertEqual(result, 80000)

    def test_apply_new_os_promo_on_os_14(self):
        app = YummyApp(os_version=14)

        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")

    def test_apply_invalid_promo_code(self):
        app = YummyApp()

        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "SAI_MA")


class TestHardLevel(unittest.TestCase):
    """Kiem thu tim nha hang bang GPS gia lap."""

    def setUp(self):
        self.app = YummyApp()

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_restaurants_inside_supported_area(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)

        result = self.app.get_nearby_restaurants()

        self.assertEqual(
            result,
            [
                "Nha hang Pho Ly Quoc Su",
                "Bun cha Huong Lien",
            ],
        )

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_restaurants_outside_supported_area(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)

        result = self.app.get_nearby_restaurants()

        self.assertEqual(result, [])

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_restaurants_when_gps_signal_is_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError()

        result = self.app.get_nearby_restaurants()

        self.assertEqual(result, "Khong the xac dinh vi tri.")


if __name__ == "__main__":
    unittest.main()