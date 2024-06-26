from django.shortcuts import redirect
from .models import Car
from django.http import HttpResponse, Http404
from django.db.utils import IntegrityError
import secrets
import os
from dotenv import load_dotenv

from .utils.otherfunctions import get_access_and_refresh, get_VINs, get_vehicle_dict, get_data_car, get_obtain_refresh_token


load_dotenv()


def authorize_view(request):
    """
        redirect на страницу авторизации TESLA
    """
    # Параметры для запроса авторизации
    client_id = os.getenv('CLIENT_ID')
    redirect_uri = os.getenv('REDIRECT_URL')
    scope = "openid offline_access vehicle_device_data"
    state = secrets.token_urlsafe(16)  # Генерация случайного значения для state

    # Подготовка URL для редиректа пользователя к Tesla для авторизации
    auth_url = f"https://auth.tesla.com/oauth2/v3/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}&response_type=code"

    # Редирект пользователя на страницу авторизации Tesla
    return redirect(auth_url)


def callback(request):
    try:
        # Проверяем, содержит ли запрос параметр 'code'
        authorization_code = request.GET.get('code')
        if authorization_code:
            # Получаем access_token и refresh_token
            access_token, refresh_token_new = get_access_and_refresh(authorization_code)
            print("ПЕРВЫЙ ТОКЕН", refresh_token_new)

            # Получаем список VIN номеров
            vehicle_VIN = get_VINs(access_token)
            # Получаем данные о транспортных средствах как словарь
            vehicle_dict = get_vehicle_dict(access_token, vehicle_VIN)


            # Получаем данные о транспортных средствах
            if vehicle_dict:
                for key, vehicle_data in vehicle_dict.items():
                    manufacturer, brand, model, vin, odometer_km = vehicle_data

                    # Проверяем наличие VIN в базе данных
                    if Car.objects.filter(VIN=vin).exists():
                        return HttpResponse(f"Vehicle with VIN {vin} already exists in the database.", status=400)

                    # Сохраняем данные в базу данных
                    tesla_credentials = Car(
                        manufacturer=manufacturer,
                        brand=brand,
                        model=model,
                        VIN=vin,
                        odometer=odometer_km,
                        refresh_token=refresh_token_new
                    )
                    tesla_credentials.save()

                    return HttpResponse("Vehicle data saved successfully!")

            else:
                return HttpResponse("No vehicle data received from Tesla API.", status=400)

        else:
            error_message = request.GET.get('error', 'Unknown error')
            return HttpResponse(f"Authorization failed: {error_message}", status=400)

    except IntegrityError as e:
        return HttpResponse(f"Error saving to database: {str(e)}", status=500)

    except Exception as e:
        return HttpResponse(f"Unexpected error: {str(e)}", status=500)


def obtain_data(request):
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

    return HttpResponse("Data processed successfully!")