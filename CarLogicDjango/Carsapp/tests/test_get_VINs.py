import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError

from Carsapp.utils.otherfunctions import get_VINs


class TestGetVehicleVins(unittest.TestCase):

    @patch('requests.get')
    def test_valid_response(self, mock_get):
        """
        Валидный ответ с VIN номерами транспортных средств
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
    "response": [
        {
            "id": 100021,
            "vehicle_id": 99999,
            "vin": "TEST00000000VIN01",
            "access_type": "OWNER",
            "display_name": "Owned",
            "option_codes": "TEST0,COUS",
            "granular_access": {
                "option_codes": "TEST0,COUS"
            },
            "tokens": [
                "4f993c5b9e2b937b",
                "7a3153b1bbb48a96"
            ],
            "state": "online"
        },
        {
            "id": 100022,
            "vehicle_id": 99998,
            "vin": "TEST00000000VIN02",
            "access_type": "OWNER",
            "display_name": "Owned",
            "option_codes": "TEST1,COUS",
            "granular_access": {
                "option_codes": "TEST1,COUS"
            },
            "tokens": [
                "5g993c5b9e2b937b",
                "8h3153b1bbb48a96"
            ],
            "state": "offline"
        },
        {
            "id": 100023,
            "vehicle_id": 99997,
            "vin": "TEST00000000VIN03",
            "access_type": "OWNER",
            "display_name": "Owned",
            "option_codes": "TEST2,COUS",
            "granular_access": {
                "option_codes": "TEST2,COUS"
            },
            "tokens": [
                "6i993c5b9e2b937b",
                "9j3153b1bbb48a96"
            ],
            "state": "online"
        }
    ],
        "pagination": {
            "current": 3,
            "per_page": 2,
            "count": 3,
            "pages": 2
        },
        "count": 3
    }
        mock_get.return_value = mock_response

        access_token = "dummy_token"
        vins = get_VINs(access_token)
        self.assertEqual(vins, ["TEST00000000VIN01", "TEST00000000VIN02", "TEST00000000VIN03"])

    @patch('requests.get')
    def test_empty_vehicle_list(self, mock_get):
        """
            Пустой список транспортных средств
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": []}
        mock_get.return_value = mock_response

        access_token = "dummy_token"
        response = get_VINs(access_token)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Vehicle list is empty or has an invalid format", response.content.decode())

    @patch('requests.get')
    def test_malformed_response(self, mock_get):
        """
            Ошибка в ответе API (Отсутствует ключ 'response')
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"wrong_key": []}
        mock_get.return_value = mock_response

        access_token = "dummy_token"
        response = get_VINs(access_token)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Vehicle list is empty or has an invalid format", response.content.decode())

    @patch('requests.get')
    def test_request_exception(self, mock_get):
        """
            Ошибка запроса (например, отказано в доступе, ошибка сервера и т.д.)
        """
        mock_get.side_effect = HTTPError("Unexpected error")
        access_token = "dummy_token"
        response = get_VINs(access_token)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Unexpected error", response.content.decode())