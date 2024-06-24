from django.urls import path
from . import views


urlpatterns = [
    path('authorize/', views.authorize_view, name='authorize'),
    path('callback/', views.callback, name='callback'),
]