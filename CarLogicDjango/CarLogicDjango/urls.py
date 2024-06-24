from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import os


def serve_public_key(request):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.well-known', 'appspecific', 'com.tesla.3p.public-key.pem')
    with open(file_path, 'r') as f:
        key_content = f.read()
    return HttpResponse(key_content, content_type='text/plain')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Carsapp.urls')),
    path('.well-known/appspecific/com.tesla.3p.public-key.pem', serve_public_key, name='serve_public_key'),
]
