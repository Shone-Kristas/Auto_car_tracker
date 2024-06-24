import unittest
from unittest.mock import patch
from Carsapp.utils.otherfunctions import get_vehicle_dict, get_data_car

class TestGetVehicleData(unittest.TestCase):

    @patch('Carsapp.utils.otherfunctions.get_data_car')
    def test_single_vehicle_vin(self, mock_get_data_car):
        """
            Проверяет успешный сценарий для одного VIN номера.
        """
        mock_get_data_car.return_value = ("Tesla", "Tesla", "Model S", "TEST00000000VIN01", 80000.0)

        access_token = "dummy_token"
        vehicle_vin = ["TEST00000000VIN01"]

        result = get_vehicle_dict(access_token, vehicle_vin)

        expected_result = {1: ("Tesla", "Tesla", "Model S", "TEST00000000VIN01", 80000.0)}
        self.assertEqual(result, expected_result)

    @patch('Carsapp.utils.otherfunctions.get_data_car')
    def test_multiple_vehicle_vins(self, mock_get_data_car):
        """
            Тестирует успешный сценарий для нескольких VIN номеров.
        """
        mock_get_data_car.side_effect = [
            ("Tesla", "Tesla", "Model S", "TEST00000000VIN01", 80000.0),
            ("Tesla", "Tesla", "Model 3", "TEST00000000VIN02", 60000.0)
        ]

        access_token = "dummy_token"
        vehicle_vin = ["TEST00000000VIN01", "TEST00000000VIN02"]

        result = get_vehicle_dict(access_token, vehicle_vin)

        expected_result = {
            1: ("Tesla", "Tesla", "Model S", "TEST00000000VIN01", 80000.0),
            2: ("Tesla", "Tesla", "Model 3", "TEST00000000VIN02", 60000.0)
        }
        self.assertEqual(result, expected_result)

    @patch('Carsapp.utils.otherfunctions.get_data_car')
    def test_empty_vehicle_vin_list(self, mock_get_data_car):
        """
            Проверяет сценарий, когда список VIN номеров пустой.
        """
        access_token = "dummy_token"
        vehicle_vin = []

        result = get_vehicle_dict(access_token, vehicle_vin)

        expected_result = {}
        self.assertEqual(result, expected_result)