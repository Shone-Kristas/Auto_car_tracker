from django.shortcuts import redirect
from .models import Car
from django.http import HttpResponse
from django.db.utils import IntegrityError
import secrets
import os
from dotenv import load_dotenv

from .utils.otherfunctions import get_access_and_refresh, get_VINs, get_vehicle_dict

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

            # Получаем список VIN номеров
            vehicle_VIN = get_VINs(access_token)
            # Получаем данные о транспортных средствах как словарь
            vehicle_dict = get_vehicle_dict(access_token, vehicle_VIN)


            # Получаем данные о транспортных средствах
            if vehicle_dict:
                for key, vehicle_data in vehicle_dict.items():
                    print(f"Vehicle data for key {key}: {vehicle_data}")
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