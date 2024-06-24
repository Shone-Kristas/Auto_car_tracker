# import unittest
# from unittest.mock import patch, MagicMock
# from django.test import RequestFactory
# from django.http import HttpResponse
# from django.db import IntegrityError
# from Carsapp.utils.otherfunctions import get_access_and_refresh, get_VINs, get_vehicle_dict
# from Carsapp.models import Car
# from Carsapp.views import callback
#
#
# class CallbackTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     @patch('Carsapp.utils.otherfunctions.get_access_and_refresh')
#     @patch('Carsapp.utils.otherfunctions.get_VINs')
#     @patch('Carsapp.utils.otherfunctions.get_vehicle_dict')
#     @patch.object(Car.objects, 'filter')
#     @patch.object(Car.objects, 'create')
#     def test_callback_success(self, mock_create, mock_filter, mock_get_vehicle_dict, mock_get_VINs,
#                               mock_get_access_and_refresh):
#         # Mock данные и объекты
#         mock_create.return_value = MagicMock()
#         mock_filter.return_value.exists.return_value = False
#         mock_get_vehicle_dict.return_value = {
#             1: ("Tesla", "Tesla", "Model S", "TEST00000000VIN01", 80000.0)
#         }
#         mock_get_VINs.return_value = ["TEST00000000VIN01"]
#         mock_get_access_and_refresh.return_value = ("dummy_access_token", "dummy_refresh_token")
#
#         # Создание запроса с параметром 'code'
#         request = self.factory.get('/callback', {'code': 'dummy_code'})
#
#         # Вызов функции callback
#         response = callback(request)
#
#         print("Response content:", response.content.decode())
#
#         # Проверки
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Vehicle data saved successfully!", response.content.decode())
#
#         # Проверяем вызовы моков
#         mock_get_access_and_refresh.assert_called_once_with('dummy_code')
#         mock_get_VINs.assert_called_once_with('dummy_access_token')
#         mock_get_vehicle_dict.assert_called_once_with('dummy_access_token', ["TEST00000000VIN01"])
#         mock_filter.assert_called_once_with(VIN="TEST00000000VIN01")
#         mock_create.assert_called_once()

    # @patch('your_module.get_access_and_refresh')
    # def test_callback_no_code(self, mock_get_access_and_refresh):
    #     # Mock функции get_access_and_refresh
    #     mock_get_access_and_refresh.return_value = ("dummy_access_token", "dummy_refresh_token")
    #
    #     # Создание запроса без параметра 'code'
    #     request = self.factory.get('/callback')
    #
    #     # Вызов функции callback
    #     response = callback(request)
    #
    #     # Проверки
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("Authorization failed", response.content.decode())
    #
    #     # Проверяем вызовы моков
    #     mock_get_access_and_refresh.assert_not_called()
    #
    # @patch('your_module.get_access_and_refresh')
    # @patch.object(Car.objects, 'filter')
    # def test_callback_vehicle_exists(self, mock_filter, mock_get_access_and_refresh):
    #     # Mock функции get_access_and_refresh
    #     mock_get_access_and_refresh.return_value = ("dummy_access_token", "dummy_refresh_token")
    #
    #     # Mock Car.objects.filter чтобы вернуть True (запись существует)
    #     mock_filter.return_value.exists.return_value = True
    #
    #     # Создание запроса с параметром 'code'
    #     request = self.factory.get('/callback', {'code': 'dummy_code'})
    #
    #     # Вызов функции callback
    #     response = callback(request)
    #
    #     # Проверки
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("Vehicle with VIN", response.content.decode())
    #
    #     # Проверяем вызовы моков
    #     mock_get_access_and_refresh.assert_called_once_with('dummy_code')
    #     mock_filter.assert_called_once_with(VIN="TEST00000000VIN01")
    #
    # @patch('your_module.get_access_and_refresh')
    # @patch.object(Car.objects, 'create')
    # def test_callback_database_error(self, mock_create, mock_get_access_and_refresh):
    #     # Mock функции get_access_and_refresh
    #     mock_get_access_and_refresh.return_value = ("dummy_access_token", "dummy_refresh_token")
    #
    #     # Mock Car.objects.create чтобы вызвать IntegrityError
    #     mock_create.side_effect = IntegrityError("Database error")
    #
    #     # Создание запроса с параметром 'code'
    #     request = self.factory.get('/callback', {'code': 'dummy_code'})
    #
    #     # Вызов функции callback
    #     response = callback(request)
    #
    #     # Проверки
    #     self.assertEqual(response.status_code, 500)
    #     self.assertIn("Error saving to database", response.content.decode())
    #
    #     # Проверяем вызовы моков
    #     mock_get_access_and_refresh.assert_called_once_with('dummy_code')
    #     mock_create.assert_called_once()
    #
    # @patch('your_module.get_access_and_refresh')
    # @patch('your_module.get_VINs')
    # @patch('your_module.get_vehicle_dict')
    # def test_callback_api_error(self, mock_get_vehicle_dict, mock_get_VINs, mock_get_access_and_refresh):
    #     # Mock функции get_access_and_refresh, get_VINs и get_vehicle_dict
    #     mock_get_access_and_refresh.side_effect = Exception("API error")
    #     mock_get_VINs.return_value = ["TEST00000000VIN01"]
    #     mock_get_vehicle_dict.return_value = None
    #
    #     # Создание запроса с параметром 'code'
    #     request = self.factory.get('/callback', {'code': 'dummy_code'})
    #
    #     # Вызов функции callback
    #     response = callback(request)
    #
    #     # Проверки
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("No vehicle data received from Tesla API", response.content.decode())
    #
    #     # Проверяем вызовы моков
    #     mock_get_access_and_refresh.assert_called_once_with('dummy_code')
    #     mock_get_VINs.assert_called_once_with('dummy_access_token')
    #     mock_get_vehicle_dict.assert_called_once_with('dummy_access_token', ["TEST00000000VIN01"])