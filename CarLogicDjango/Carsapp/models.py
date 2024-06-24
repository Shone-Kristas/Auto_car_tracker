from django.db import models


class Car(models.Model):
    manufacturer = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    VIN = models.CharField(max_length=17, unique=True)  # Уникальное значение
    odometer = models.FloatField(default=0)
    refresh_token = models.CharField(max_length=255, unique=True)  # Предполагаем, что это строка для хранения токена

    def __str__(self):
        return f"manufacturer: {self.manufacturer} brand: {self.brand} model: {self.model} VIN: {self.VIN} Odometer: {self.odometer} refresh_token: {self.refresh_token}"