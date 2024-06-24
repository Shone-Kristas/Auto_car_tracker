import unittest
from unittest.mock import patch, MagicMock

from Carsapp.utils.otherfunctions import get_data_car

class TestGetDataCar(unittest.TestCase):

    @patch('requests.get')
    def test_successful_response(self, mock_get):
        """
            Тестирует успешный сценарий для нескольких.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
                     "response": {
                      "id": 100021,
                      "user_id": 800001,
                      "vehicle_id": 99999,
                      "vin": "TEST00000000VIN01",
                      "access_type": "OWNER",
                      "tokens": [
                       "4f993c5b9e2b937b",
                       "7a3153b1bbb48a96"
                      ],
                      "state": "online",
                      "id_s": "100021",
                      "api_version": 54,
                      "charge_state": {
                       "battery_level": 42,
                       "usable_battery_level": 42,
                      },
                      "climate_state": {
                       "cabin_overheat_protection": "On",
                       "timestamp": 1692141038419,
                      },
                      "drive_state": {
                       "active_route_latitude": 37.7765494,
                       "timestamp": 1692141038420
                      },
                      "gui_settings": {
                       "gui_charge_rate_units": "mi/hr",
                       "timestamp": 1692141038420
                      },
                      "vehicle_config": {
                       "aux_park_lamps": "NaPremium",
                       "car_type": "modely",
                       "wheel_type": "Apollo19"
                      },
                      "vehicle_state": {
                       "api_version": 54,
                       "last_autopark_error": "no_error",
                       "media_info": {
                        "a2dp_source_name": "Pixel 6",
                        "now_playing_title": "PBS Newshour"
                       },
                       "media_state": {
                       },
                       "odometer": 15720.074889,
                       "santa_mode": 0,
                       "software_update": {
                        "download_perc": 0,
                        "version": " "
                       },
                       "speed_limit_mode": {
                        "current_limit_mph": 85,
                        "max_limit_mph": 120,
                        "min_limit_mph": 50,
                       },
                       "timestamp": 1692141038419,
                       "tpms_last_seen_pressure_time_fl": 1692136878,
                       "vehicle_self_test_progress": 0,
                      }
                     }
                    }
        mock_get.return_value = mock_response

        access_token = "dummy_token"
        vehicle_vin = "TEST00000000VIN01"
        result = get_data_car(access_token, vehicle_vin)

        expected_result = ("Tesla", "Tesla", "modely", vehicle_vin, 15720.074889 * 1.60934)
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_missing_model(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
             "response": {
             }
            }
        mock_get.return_value = mock_response

        access_token = "dummy_token"
        vehicle_vin = "TEST00000000VIN01"
        response = get_data_car(access_token, vehicle_vin)

        self.assertEqual(response.status_code, 500)
        self.assertIn("Unexpected error", response.content.decode())