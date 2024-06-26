import requests
from django.http import HttpResponse, Http404
import os
from dotenv import load_dotenv


def get_access_and_refresh(auth_code: str):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv('CLIENT_ID'),
        "client_secret": os.getenv('CLIENT_SECRET'),
        "code": auth_code,
        "audience": os.getenv('TESLA_API_AUDIENCE'),
        "redirect_uri": os.getenv('REDIRECT_URL')
    }
    try:
        response = requests.post(os.getenv('TESLA_TOKEN_URL'), headers=headers, data=data)
        response.raise_for_status()

        response_json = response.json()
        access_token = response_json.get("access_token")
        refresh_token = response_json.get("refresh_token")

        return access_token, refresh_token
    except Exception as e:
        return HttpResponse(f"Unexpected error: {e}")


def get_VINs(access_token: str):
    url = f"https://fleet-api.prd.eu.vn.cloud.tesla.com/api/1/vehicles"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        vehicle_data = response.json()
        vehicles = vehicle_data.get('response', [])

        if isinstance(vehicles, list) and vehicles:
            vehicle_vins = [vehicle.get('vin') for vehicle in vehicles if vehicle.get('vin')]
            return vehicle_vins
        else:
            raise Http404("Vehicle list is empty or has an invalid format")

    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")


def get_vehicle_dict(access_token: str, vehicle_vin: list):
    try:
        vehicle_data_dict = {}
        if len(vehicle_vin) == 1:
            vehicle_data_dict[1] = get_data_car(access_token, vehicle_vin[0])
        else:
            for i in range(len(vehicle_vin)):
                vehicle_data_dict[i+1] = get_data_car(access_token, vehicle_vin[i])
        return vehicle_data_dict
    except ValueError as e:
        raise ValueError(f"Error fetching vehicle data: {e}")


def get_data_car(access_token: str, vehicle_vin: str):
    url = f'https://fleet-api.prd.eu.vn.cloud.tesla.com/api/1/vehicles/{vehicle_vin}/vehicle_data'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        vehicle_data = response.json()
        vehicle_manufacturer = "Tesla"
        vehicle_brand = "Tesla"
        vehicle_model = vehicle_data.get('response', {}).get('vehicle_config', {}).get('car_type')
        odometer_miles = vehicle_data.get('response', {}).get('vehicle_state', {}).get('odometer')

        if vehicle_model is None or odometer_miles is None:
            raise ValueError("Missing vehicle data in the response")

        odometer_km = odometer_miles * 1.60934
        return vehicle_manufacturer, vehicle_brand, vehicle_model, vehicle_vin, odometer_km

    except requests.exceptions.HTTPError as http_err:
        status_code = response.status_code if response else None
        if status_code == 404:
            raise ValueError(f"Vehicle with VIN '{vehicle_vin}' not found")
        else:
            raise ValueError(f"HTTP error occurred: {http_err}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")


def get_obtain_refresh_token(token):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv('CLIENT_ID'),
        "refresh_token": token
    }
    try:
        response = requests.post(os.getenv('TESLA_TOKEN_URL'), headers=headers, data=data)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            response_json = response.json()
            new_access_token = response_json.get("access_token")
            new_refresh_token = response_json.get("refresh_token")

            if not new_access_token or not new_refresh_token:
                print("Missing access_token or refresh_token in response.")
                return None, None
            return new_access_token, new_refresh_token
        else:
            print(f"Response did not contain JSON data. Content-Type: {content_type}")
            return None, None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None, None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None, None