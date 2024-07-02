from django.urls import path
from . import views


urlpatterns = [
    path('authorize/', views.authorize_view, name='authorize'),
    path('callback/', views.callback, name='callback'),
    # path('obtain_data/', views.obtain_data, name='obtain_data'),
]