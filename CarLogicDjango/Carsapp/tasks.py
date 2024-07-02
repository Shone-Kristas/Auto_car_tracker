from .utils.otherfunctions import get_data_car, get_obtain_refresh_token
from .models import Car
from django.http import Http404
from celery import shared_task



@shared_task
def obtain_data():
    cars_data = list(Car.objects.values_list('VIN', 'odometer', 'refresh_token'))

    for vin, odometer, refresh_token in cars_data:
        try:
            access_token, new_refresh_token = get_obtain_refresh_token(refresh_token)

            if not access_token or not new_refresh_token:
                print(f"Failed to obtain tokens: {refresh_token}, for VIN: {vin}")
                continue

            if new_refresh_token:
                Car.objects.filter(VIN=vin).update(refresh_token=new_refresh_token)

            vehicle_data = get_data_car(access_token, vin)

            if vehicle_data:
                _, _, _, _, odometer_km = vehicle_data
                if odometer != odometer_km:
                    Car.objects.filter(VIN=vin).update(odometer=odometer_km)

        except Http404 as e:
            print(f"Http404 Exception occurred for VIN {vin}: {e}")

        except Exception as e:
            print(f"Unexpected error occurred for VIN {vin}: {e}")

    return print('good')